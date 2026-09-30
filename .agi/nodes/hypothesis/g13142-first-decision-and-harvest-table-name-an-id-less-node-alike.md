---
id: hypothesis:g13142-first-decision-and-harvest-table-name-an-id-less-node-alike
mint_id: ed4041d5f8bb4847a5152d63519fe513
type: hypothesis
parents:
  - goal:g1.31.4.2.1
next_edges: []
scaffold_hash: 0eda4fa6debdd73e
season: 2
testable_claim: for an id-less kid node, first-decision and cmd_harvest_table print the same name via one shared helper; the strict-xfail row at test_rotate_first_decision_residues.py:200 passes without its marker
title: first-decision and harvest-table name every kid node through one helper, id-less nodes included
town: core
---

# hypothesis:g13142-first-decision-and-harvest-table-name-an-id-less-node-alike

## Measured
- DG4.14c (70599a543b) test_rotate_first_decision_residues.py:200: `xfail(strict=True)` pins a LIVE defect: for a kid node WITHOUT an `id:` field, the first-decision reader (rotate.py ~17386, `f.get("id") or f"experiment:{stem}"`) names it `experiment:<stem>`, while `cmd_harvest_table` (rotate.py ~21712) prints the same node as its `.md` relpath -- two readers of one round disagree on one node's name.
- found by the DG4.14c kid (Sonnet 5.5) turning the pi mur-director-general-4-15 M1 residue (a green row that required the disagreement) into a readers-agree row.

## CLAIM
first-decision and harvest-table name every kid node identically, id-less nodes included, through ONE naming helper both call; the strict-xfail row at test_rotate_first_decision_residues.py:200 passes (its xfail marker removed).

## Dispatch line
config-max: none / template-max: none / code: one shared node-name helper in rotate.py used by both readers.

## FALSIFIERS
1. The xfail row still fails without its marker, or any first-decision / harvest-table row changes its output for an id-carrying node.
2. A second naming site for kid nodes remains in either reader.

## TESTS
test_rotate_first_decision*.py + test_bin_help_smoke.py (+ any harvest-table test found with git grep cmd_harvest_table -- extensions/agi/tests).

## FILE SCOPE
extensions/agi/bin/rotate.py (the two readers + one helper), extensions/agi/tests/test_rotate_first_decision_residues.py (drop the xfail marker only).

## CEILING
1 kid · <= 12 prod lines · <= 5 test lines.
