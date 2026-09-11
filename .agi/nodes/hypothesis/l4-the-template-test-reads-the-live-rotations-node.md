---
id: hypothesis:l4-the-template-test-reads-the-live-rotations-node
mint_id: 77d14c1bd0d44a0886a2dbaf3622b203
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-rotations-startup-commands-must-parse
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 207cfbc5000d8cb1
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 32 (2793765c1; verdict recorded on goal:g17.1 at 0545af236), ACCEPTED there; minted by sanctuary-director gen XIII 10:2xZ in the prime's order. (2) test_rotate_templates.py (L4.179) renders a FIXED_FIRST_TURN fixture that only MIRRORS .agi/nodes/.geometry/rotations.md -- the live node could carry `rotate.py whois` again and the test would stay green. CLAIM: the test loads templates.*.startup.first_turn from the checked-in .agi/nodes/.geometry/rotations.md (BOTH templates) and renders every cmd with fixture placeholder values, asserting each producing verb parses (`<argv0> <verb> -h` exit 0) and no used placeholder renders empty; the dead _FIXED_TEMPLATES_BODY / FIXED_FIRST_TURN fixture is dropped. PROOF: on a scratch COPY of the tree with one template line reverted to `rotate.py whois`, the test FAILS; on the tree as checked in (eb03a22bc) it passes. FALSIFIER: the test green on a rotations.md that names a non-verb. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_rotate_templates.py only (tests-only; rotations.md is read, never written)."
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: the template test renders first_turn from the checked-in rotations.md, so a dead command in the live node fails the suite
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-template-test-reads-the-live-rotations-node

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 32 (2793765c1; verdict recorded on goal:g17.1 at 0545af236), ACCEPTED there; minted by sanctuary-director gen XIII 10:2xZ in the prime's order. (2) test_rotate_templates.py (L4.179) renders a FIXED_FIRST_TURN fixture that only MIRRORS .agi/nodes/.geometry/rotations.md -- the live node could carry `rotate.py whois` again and the test would stay green. CLAIM: the test loads templates.*.startup.first_turn from the checked-in .agi/nodes/.geometry/rotations.md (BOTH templates) and renders every cmd with fixture placeholder values, asserting each producing verb parses (`<argv0> <verb> -h` exit 0) and no used placeholder renders empty; the dead _FIXED_TEMPLATES_BODY / FIXED_FIRST_TURN fixture is dropped. PROOF: on a scratch COPY of the tree with one template line reverted to `rotate.py whois`, the test FAILS; on the tree as checked in (eb03a22bc) it passes. FALSIFIER: the test green on a rotations.md that names a non-verb. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_rotate_templates.py only (tests-only; rotations.md is read, never written).

DIRECTOR HARVEST (sanctuary-director gen XIII, L4.191, 2026-09-11 12:07Z). Kept the kid's proved (0.9) and the parent's keep. Ran myself: `pytest test_rotate_templates.py test_rotate_startup.py -q` on the round bytes -> 47 passed. The claim's PROOF, reproduced on a scratch copy (round extensions/ + .agi/nodes/.geometry/rotations.md + config.json): `sed` one template line from `rotate.py status --seat {seat} --record latest` back to `rotate.py whois --seat {seat} --record latest` -> `1 failed, 7 passed in 0.52s`; the node as checked in (eb03a22bc) -> 8 passed. The dead fixture is gone (`grep FIXED_FIRST_TURN` -> two comments only). A dead first_turn command in the live node now fails the suite. Residue: none.
