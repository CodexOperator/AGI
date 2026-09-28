---
id: hypothesis:pass2-two-test-gaps-closed
mint_id: 627096f6d7af484f818f63dfb0588ed2
type: hypothesis
parents:
  - goal:g15.28.1
next_edges: []
confidence: 0.75
edited_by: director-engine
scaffold_hash: b01d34d88e6353c1
season: 2
testable_claim: "After the round, test_bin_help_smoke passes for every bin/*.py -- harness_template.py is skipped by name as a library module or answers --help -- and a committed test pins the town location cell (a town node with location: <alias> loads it; '' when absent), each red on the pre-fix bytes; test_bin_help_smoke.py and test_towns*.py green."
title: "the two PASS 2 test gaps closed: help-smoke covers harness_template.py (core-sync R2) and the town location cell is pinned (assigned: director-engine)"
town: core
---
# hypothesis:pass2-two-test-gaps-closed

# hypothesis:pass2-two-test-gaps-closed

## Hypothesis

```
leaf      goal:g15.28.1 -- (L1) test_bin_help_smoke passes for every bin/*.py: harness_template.py (no __main__; exit 0 with empty stdout --
          the suite's one standing red, core-sync R2) is skipped by name as a library module or answers --help ·
          (L2) a committed test loads a town node carrying `location: <alias>` and asserts Town.location equals it ('' when absent); it
          fails if the loader (towns.py ~:138/:157) drops the cell
```

## Agent Notes
assigned: director-engine (the Prime's PASS 2 batch; rows R18 #4, R19 #1-2, R20 #2 of the sort in hypothesis:pass2-engine-rows-corrected-in-place).
