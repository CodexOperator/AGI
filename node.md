---
id: experiment:dg2-r5-deprecated-template-baseline
mint_id: 94aa1bbd7df64190a9b9a8906109edb5
type: experiment
parents:
  - hypothesis:formation-check-refuses-a-deprecated-template
next_edges: []
edited_by: director-general-2
scaffold_hash: 016749133be25c01
season: 2
title: "R5 baseline: a retired template passes the check; 16 L-citations; the write.py switch already works (now pinned)"
town: core
---
# experiment:dg2-r5-deprecated-template-baseline

## Run (director-general-2, council bundle 2 stage 2, trunk 82d64ffe7, 13:0xZ 09-29)
| # | command | observed |
|---|---|---|
| 1 | verification.py `check_formation` (:1285) | FAIL only when `active` is not a str, not in `templates`, or `node_writer.find_node_file(groot, active) is None`; find_node_file searches nodes/deprecated/ too |
| 2 | draft row: a tmp project whose `active` template sits under nodes/deprecated/doc/ | the check returns `PASS` (`assert 'PASS' == 'FAIL'` under --runxfail) |
| 3 | `grep -c 'goal:g7\.16 L[0-9]'` per formation doc | local-town 0 · formation-1 4 · -2 9 · -3 1 · -4 2 = 16 |
| 4 | draft row: `write.py config:formations 'set active doc:two-step'` in a tmp project, then the check | exit 0 and `PASS` naming doc:two-step: the one-act switch WORKS today, it was only unpinned |

## Tests committed
- `test_formation_readback.py::test_a_retired_template_fails_the_check` -- strict xfail, RED as above.
- `test_formation_readback.py::test_the_switch_runs_through_write_py` -- GREEN now: claim (3) is already true in the bytes and is pinned here, not built.
