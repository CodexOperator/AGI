---
id: hypothesis:spawn-budget-acquire-refuses-a-harness-at-its-row-max-live
mint_id: c31705cb321f41d5badb6f946d029e59
type: hypothesis
parents:
  - goal:g5.27
next_edges: []
edited_by: director-engine
scaffold_hash: ae01601dcc5f8df5
season: 2
testable_claim: With harnesses.pi-local.max_live = 1 and one live pi-local lease, acquire(..., harness=pi-local) returns None and names pi-local (1/1), while harness=pi and bare acquires still admit.
title: spawn_budget.acquire records the lease's harness and refuses by name at harnesses.<h>.max_live (leaf 1/2 of TMM.82's per-harness max_live)
town: local-maxxing
---
# hypothesis:spawn-budget-acquire-refuses-a-harness-at-its-row-max-live

## Measured
- spawn_budget.py:535-536 -- `acquire(root, cap, agent_id, tier, iter_n)` takes no harness; the lease rec (:581-588) carries none,
  nor do commit (:640-649) / attach_branch (:618-637).
- :575-591 -- sweep, count and write are ONE step under `_budget_lock`: the only race-free place for a per-harness cap (the 01:29Z
  race was two directors each reading "0 live" by hand). :561-563 already loads config; the load gate :564-574 refuses by name and
  returns None -- the precedent. No harness row carries max_live yet; only spawn.max_live (30). (goal:g4.8 = the tree-wide bound.)
## CLAIM
`acquire(..., harness=None)` records "harness" on the lease; under the lock it returns None and prints
`spawn_budget: refusing <id> -- harness <h> at max_live (<n>/<m>)` once that harness's live leases reach its row's `max_live`.
No harness, or no cell -> unchanged.
## Dispatch line
config-max: the cap is the ROW cell harnesses.<h>.max_live, never a literal / template-max: none / code: spawn_budget.py acquire() only
## FALSIFIERS
- a second pi-local acquire is admitted, or a pi / bare one is refused
- a test_spawn_budget.py test goes red (56 passed on 64e9858bb9); a harness-name literal in the check
## TESTS
test_spawn_budget.py::test_acquire_refuses_a_harness_at_its_row_max_live -- root/.agi/config.json {"harnesses": {"pi-local":
{"max_live": 1}}} (the _gated_root pattern, :218-223); the first pi-local acquire is admitted with harness == "pi-local" on its
lease; the second returns None and stderr names "pi-local" and "(1/1)"; harness="pi" and bare acquires admit. Red today (unexpected
kwarg). Neighbours: test_dispatch.py, test_provisioning.py.
## FILE SCOPE
extensions/agi/bin/spawn_budget.py 535-596
extensions/agi/tests/test_spawn_budget.py 33-50, 218-265
## CEILING
1 kid (--harness pi-free until the free lane opens; never pi-local) · 10 production lines · 0 USD · FIRST of two
