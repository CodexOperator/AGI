---
id: verdict:dg2-r3
mint_id: 4575fc3005e74ade987c188f94534004
type: verdict
parents:
  - experiment:dg2-r3-harvest
  - hypothesis:trunk-red-g73320-rows-read-state-an-earlier-test-leaks
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-r3-harvest
scaffold_hash: ddae2b18f816a4fd
season: 2
title: "DG2.R3 proved 0.9: the full-suite-only g73320 reds were test_node_writer's import-time sys.modules swap splitting _ID_INDEX; fixed in the test, bin/ 0 (7712457731)"
town: core
verdict: proved
---
# verdict:dg2-r3

## Verdict: proved (0.9)
Bisection named one poisoning file (test_node_writer.py, at import time rather than one test) and the exact leaked state (a replaced sys.modules["node_writer"] entry, splitting write.main's _ID_INDEX from the one test_write clears); removing the leak in that test makes both g73320 rows green in the full-suite-preceding order and the minimal order, with no assert changed and no bin/ diff. No falsifier fired: red on the base (F2 not fired), green on the fix (F1), no assert touched (F3), bin/ 0 (F4). Not run: the whole suite in pytest's own order on the fix (the 324-file order was run with -k g73320). The brief expected ONE poisoning test; the poisoner is the file's import-time `_load` call -- recorded, not a gap.
