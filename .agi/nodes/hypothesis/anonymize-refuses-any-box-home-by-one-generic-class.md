---
id: hypothesis:anonymize-refuses-any-box-home-by-one-generic-class
mint_id: ab87a525f4934d6083ad2fef5a684f66
type: hypothesis
parents:
  - goal:g7.16.1.2.3
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: 1f2eebf9dcb16c50
season: 2
tags:
  - council-loop
  - bundle-2
  - row-r3
testable_claim: (1) one generic home class, no literal home value, refused by scan and check (2) a test row each for /home and /Users (3) every matching file under .agi/nodes, datasets and .agi/sessions/quorum scrubbed in the same round (4) the master-gate skill points at the classes
title: "anonymize.py refuses any box home path by ONE generic /home|/Users class; every matching node, dataset and quorum file scrubbed in the same round (row R3; assigned: director-general-3)"
town: core
---
# hypothesis:anonymize-refuses-any-box-home-by-one-generic-class

## Measured
- anonymize.py's home token (bundle 1 row C) is THIS box's home value only. Other boxes' home paths pass `check`.
- `git grep -lE '/(home|Users)/[^/<]+/'` at 12:5xZ 09-29: 377 files under .agi/nodes (374 live), 34 under datasets/, 16 under .agi/sessions/quorum.
- skills/agi-master-gate/SKILL.md copies path classes instead of pointing at anonymize.py.

## CLAIM
(1) anonymize.py carries ONE generic home class, `/(home|Users)/<segment>/`, that `scan` and `check` refuse on any box, with no literal home value in the file. (2) One test row each for `/home/<x>/` and `/Users/<x>/`. (3) The same round scrubs every matching file under .agi/nodes (through write.py), datasets/ and .agi/sessions/quorum to `<home>/`. (4) The master-gate skill names anonymize.py's classes instead of copying them.

## Dispatch line
config-max: none. A home class is a pattern, not a value, and a value in config is the leak. template-max: the master-gate skill line becomes a pointer. code: the one generic class in anonymize.py's existing token/class path.

## FALSIFIERS
- `check` passes a staged `/home/<someone>/x` or `/Users/<someone>/x`.
- Any matching file remains in the three scopes.
- anonymize.py gains an exemption or ignore list.

## TESTS
extensions/agi/tests/test_anonymize_guard.py (+2 rows) + `test_bin_help_smoke.py`, `--basetemp /tmp/b2r3`

## FILE SCOPE
extensions/agi/bin/anonymize.py · extensions/agi/tests/test_anonymize_guard.py · skills/agi-master-gate/SKILL.md (as a build version) · the matching files under .agi/nodes (write.py) · datasets/ · .agi/sessions/quorum

## CEILING
no dispatch · <= 10 production lines · <= 25 test lines · 0 USD · scrub is text-only (node count unchanged)
