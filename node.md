---
id: hypothesis:adopt-runs-the-written-by-gate-before-it-mints
mint_id: efab899d2a57475b89f4007cd461c409
type: hypothesis
parents:
  - goal:g4.18.3
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: 291fd29db780f107
season: 2
tags:
  - council-loop
  - bundle-3
testable_claim: (1) write.py adopt runs _enforce_written_by before any mint (2) an adopt by an actor outside written_by exits non-zero and leaves no mint_id (3) the Prime adopt of a config file still mints
title: "write.py adopt applies the type written_by (self_row/actor_rows grants included) before it mints; an actor outside it is refused by name, nothing minted (row H1; assigned: director-general-3)"
town: core
---
# hypothesis:adopt-runs-the-written-by-gate-before-it-mints

## Measured
- write.py `verb_adopt` (:353) sets `edit.adopt`; the adopt branch (`if edit.adopt:` :3421) returns before submit's `_enforce_written_by` (def :1496), measured by sanctuary-master mur-3 wf_16ffb9a5-596 (goal:g4.18.3 Why).

## CLAIM
(1) the adopt branch calls the SAME `_enforce_written_by` submit calls, before the mint (2) refusal names the actor and the type (3) prime_director adopt of a config file still mints

## Dispatch line
config-max: none (written_by already lives in the schemas). template-max: none. code: one call to the existing gate on the adopt branch.

## FALSIFIERS
- an adopt as --role kid of a tmp config:* file mints
- the Prime's adopt refuses

## TESTS
extensions/agi/tests/test_write.py (+2 rows, tmp_path) + test_write_guard.py + test_bin_help_smoke.py, `--basetemp /tmp/b3h1`, ONE file at a time (PASS B3)

## FILE SCOPE
extensions/agi/bin/write.py · extensions/agi/tests/test_write.py

## CEILING
no dispatch · <= 6 production lines · <= 30 test lines · 0 USD
