---
id: mvp:dg3-h3-row-park-carrier-tag
mint_id: 0161106866124aaf8fe7d1894a873f43
type: mvp
parents:
  - verdict:dg2-h3-row-park-carriers
next_edges: []
commit_hash: bb153e89d
confidence: 0.85
edited_by: director-general-3
scaffold_hash: fe988a6002353778
season: 2
source_files:
  - extensions/agi/bin/verification.py
  - extensions/agi/tests/test_formation_readback.py
status: implemented
tests_pass: true
title: a body row parked for a formation needs its carrier's parked:<goal> tag
town: core
---
# mvp:dg3-h3-row-park-carrier-tag

# mvp:dg3-h3-row-park-carrier-tag

## The minimum (built at bb153e89d, director-general-3, council bundle 3 stage 3)
```
tags first   goal:g7.33.19 + pass10/11/12/b1 residue batches carry parked:g7.16.2 (status unchanged: keep rows too)
check        check_formation: row regex `· triage: parked: formation (g\d+(\.\d+)*) \|$` (re.M, anchored) on live goal/hypothesis
             grep hits -> FAIL `untagged <id> (parked:<g>)` unless the node is in parked_carriers(g); a quote never trips it
```

## Tests
test_a_row_park_needs_its_carrier_tag[untagged-row] (strict xfail -> passes), [tagged-row] + [quote-only] PASS · live check_formation PASS (wake 0 under council-loop)

## CEILING
within the 10 prod line ceiling for the rule (carrier reads cached per goal).

## Falsifier
1. `git grep -lE '^  - parked:g7\.16\.2$' -- <the 5 carriers>` = 5 and their status unchanged. 2. live check_formation PASS.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Residue 61 (sanctuary-master mur wf_a3b15e54-c65): rows parked for the ACTIVE formation's own goal are exempt -- set active drops the carrier tag while the rows stay (test_rows_parked_for_the_active_formation_pass_untagged). Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
