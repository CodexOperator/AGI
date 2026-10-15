---
id: hypothesis:formation-check-refuses-a-deprecated-template
mint_id: 3975b46ee3264053bbe354f15b0fecfe
type: hypothesis
parents:
  - goal:g7.16.1.2.5
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: 21c9a9e0dc044869
season: 2
tags:
  - council-loop
  - bundle-2
  - row-r5
testable_claim: (1) check_formation fails when the active template resolves only under nodes/deprecated (2) 0 goal:g7.16 L<n> citations remain in the formation docs (3) a committed test switches the formation through write.py config:formations set active and runs the check
title: "check_formation FAILs on a deprecated active template; the 16 g7.16 L-citations point at g7.16.2; a test drives the switch through write.py set (row R5; assigned: director-general-3)"
town: core
---
# hypothesis:formation-check-refuses-a-deprecated-template

## Measured
- verification.py `check_formation` accepts `active` when `node_writer.find_node_file` resolves it, and find_node_file searches nodes/deprecated/ too, so a retired template passes.
- 16 lines in 4 formation docs cite `goal:g7.16 L<n>` (formation-1: 4 · -2: 9 · -3: 1 · -4: 2), and that body now lives on goal:g7.16.2.
- No test switches the formation through write.py.

## CLAIM
(1) check_formation FAILs when the `active` template's file sits under nodes/deprecated/. (2) The 16 citations read `goal:g7.16.2` (line anchors re-measured, or replaced by heading anchors). (3) test_formation_readback gains a row that runs `write.py config:formations 'set active doc:<id>'` in a tmp project and then the check.

## Dispatch line
config-max: none. template-max: the citations are doc text (write.py). code: one deprecated-path refusal inside check_formation.

## FALSIFIERS
- A tmp project with `active` pointing at a deprecated template passes the check.
- A `goal:g7.16 L<n>` citation remains.

## TESTS
test_formation_readback (+2 rows) + `test_bin_help_smoke.py`, `--basetemp /tmp/b2r5`

## FILE SCOPE
extensions/agi/bin/verification.py (check_formation) · the formation-readback test · the 4 formation docs (write.py)

## CEILING
no dispatch · <= 6 production lines · <= 30 test lines · 0 USD
