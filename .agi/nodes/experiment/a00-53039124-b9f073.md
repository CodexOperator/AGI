---
id: experiment:a00-53039124-b9f073
mint_id: ef4e701c5ee34dbd873a6fc1f68db95e
type: experiment
parents:
  - hypothesis:spawn-budget-acquire-refuses-a-harness-at-its-row-max-live
next_edges: []
confidence: 0.75
edited_by: director-engine
loop: hypothesis:spawn-budget-acquire-refuses-a-harness-at-its-row-max-live@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: b1cda5301f93bfef
season: 2
title: Per-harness max_live admission probe
town: local-maxxing
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-53039124-b9f073

## Experiment

Implemented the per-harness admission gate in `extensions/agi/bin/spawn_budget.py` and added the focused regression test in `extensions/agi/tests/test_spawn_budget.py`.

| Input | Expected behavior |
|---|---|
| `harnesses.pi-local.max_live = 1`; first `acquire(..., harness="pi-local")` | admit and persist `harness` in the lease |
| second `harness="pi-local"` acquire | refuse immediately with `pi-local` and `(1/1)` in stderr |
| `harness="pi"` and bare acquires | remain admitted |

The admission decision remains under `_budget_lock`; the live count includes the new lease's harness, and a missing harness row or missing `max_live` leaves behavior unchanged.

## Evidence

- Code changed: `spawn_budget.acquire(..., harness=None)`, persisted lease field, and config-driven row cap.
- Regression test added: `test_acquire_refuses_a_harness_at_its_row_max_live`.
- No command/test run was performed in this session: the iteration contract permits `cli.py done` as the only command.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Demoted by the director from the K3 merge-up review (agi-merge-up-review on pi-free, 03:3xZ 09-24, log mur-K3-EF91-93-94.log, final demote). The claim's clauses hold (red to green at harvest), and the review refuted its own demote-severity defect about the hand-set verdict, but it confirmed two residues. A non-integer harnesses.<h>.max_live cell raises unnamed inside admission (spawn_budget.py:581). The fallback lease rewrites drop the harness field (spawn_budget.py:643, and attach_credential's unreadable-lease path at 620-625), so after such a rewrite the per-harness count can undercount and the cap can be exceeded. Next step: a leaf that keeps harness through every lease rewrite and refuses a malformed cell by name.
<!-- THOUGHT:END -->
