---
id: hypothesis:l4-a-seat-rotates-at-its-own-line
mint_id: a3419f23ee324b34b96326caab8f26d6
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L4-VI
scaffold_hash: 03ff08c386a8394b
season: 2
testable_claim: "OWNER 2026-09-10 22:44Z (verbatim in doc:l4-owner-decisions): 'the sonnet helper seems to struggle past 0.3 context level, starts losing track. Maybe set it to rotate at 0.29 instead.' MEASURED: rotate.py has ONE threshold for every seat - the ladder's director_rotate_at (0.47), read by meter --check, loop, rotate-self and alarms (five call sites) - and no per-seat override; seat rows are read with .get, so config:seats sanctuary-helper now carries rotate_at 0.29 (written by the Prime at the owner's order) and the cell is INERT until this round. CLAIM: a seat rotates at its OWN line - one resolver, rotate_threshold(root, seat), returns the seat row's rotate_at when present and the ladder's director_rotate_at otherwise, and every call site that compares a fraction to a threshold goes through it: meter --check (with --seat or an explicit seat name), loop, rotate-self, and alarms (per held seat, not one threshold for the loop). The value is graph data, never a flag: no --rotate-at option, no env. PROVED BY: with a fixture seats node carrying rotate_at 0.29 for one seat and nothing for another, and a fixture transcript at fraction 0.33, meter --check exits 1 for the first seat and 0 for the second; alarms --once dms rotate now for the first only; the live helper pin (.agi/sessions/sanctuary-helper.meter) reads its own line in the meter output (threshold=0.29). DISPROVED BY: any call site still reading director_rotate_at directly, or a rotation of the helper past 0.29 after this lands. HARD RULES: rotate.py is build:bin-rotate, edited through write.py; SERIAL on rotate.py behind the 0a-0b-0c chain (the point sequences it); no new bin/*.py; the ladder default stays 0.47 for every seat without a cell (owner 2026-09-09); tests pinning the threshold are updated in the round, not skipped."
thought_session: belam-S1-L4-VI
title: A seat rotates at its OWN line — config:seats rotate_at overrides the ladder's director_rotate_at, data not flag
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-seat-rotates-at-its-own-line

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
