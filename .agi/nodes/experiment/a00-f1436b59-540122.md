---
id: experiment:a00-f1436b59-540122
mint_id: 1feece20acde4f7cab055e57fa786a66
type: experiment
parents:
  - hypothesis:l4-the-kid-tier-gate-scans-every-root-it-can-reach
next_edges: []
confidence: 0.85
edited_by: a00-06c44930
evidence_runs:
  - experiment:a00-f1436b59-540122
loop: hypothesis:l4-the-kid-tier-gate-scans-every-root-it-can-reach@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 80e653babe4a679e
season: 2
title: A00 f1436b59 540122
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f1436b59-540122

## Experiment

Closed two defects the parent measured in `experiment:a00-71de766d-07a75b`'s
multi-root scan (`hypothesis:l4-the-kid-tier-gate-scans-every-root-it-can-
reach`). The prior kid only ever run the file under its OWN runtime, where
its own kid record is the nearest ancestor, so it saw 28 green and missed
both.

DEFECT 2 (root-order dependence) — FIXED in `extensions/agi/tests/conftest.py`
`_effective_tier()`. The old code resolved the ancestor chain PER ROOT and
returned the FIRST root with any ancestor hit. Pids are process-global, so
merging every root's running record map into ONE dict before resolving the
chain once makes the outcome order-independent and lets `
_resolve_tier_from_ancestors` (nearest-first) decide. Simulated on the old
logic: [R1={111:'parent'}, R2={222:'kid'}], chain 222->111:
  ORDER R1,R2 -> 'parent' (gate cleared), ORDER R2,R1 -> 'kid' (refused)
With the merged map both orders -> 'kid'. Regression test
`test_decision_effective_tier_is_root_order_independent` (in test_tier_gate.py)
holds the process's own kid record in the later root and a distant parent in
the earlier root, asserts 'kid' for BOTH `_record_roots()` orders, and sets
AGI_TIER=parent so a host env cannot make it pass trivially.

DEFECT 1 (RED under a live parent runner) — FIXED in `test_hook_bare_directory
_kid_refused`. It ran `_run_pytest([], "kid")` with NO planted record, relying
on the AGI_TIER fallback. Under a live parent that spawned the suite, an
ambient parent record in `seat-sanctuary-director` is a running ancestor, so
the record scan supplied tier=parent and no refusal happened (assert 0==4).
Now it plants a kid record at its own `os.getpid()` — the nearest ancestor —
so merged nearest-wins deterministically refuses at any runtime. No env var
or pytest option seam was re-added (only the no-seam in-process monkeypatch
tests already use).

VERIFY:
  python3 -m pytest extensions/agi/tests/test_tier_gate.py -q
  => 29 passed (28 before, +1 regression test)

## Evidence

27/28 prior tests pass unchanged; the new order-independence regression test
(29th) fails on the old per-root code and passes on the merged-map code. The
bare-directory-refusal test now carries a plant at `os.getpid()` and is green
as this child, i.e. under the exact live-runtime shape the parent measured. Run
from the worktree as a live parent it is deterministic because nearest-wins
now keys on the planted own-pid kid record, not on scan order.

## Agent Notes
Fixed both parent-measured defects in multi-root gate scan: merged all _record_roots() pid->tier maps into one dict before ancestor resolution (order-independent, nearest-wins); hardened test_hook_bare_directory_kid_refused to plant a kid record at os.getpid() so it refuses deterministically under a live parent. Added root-order-independence regression test. test_tier_gate.py: 29 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Accepted. Merged-map fix confirmed by reading conftest.py:_effective_tier — one dict from all roots, then _resolve_tier_from_ancestors once, so the process own pid is the nearest ancestor and always wins. Regression test test_decision_effective_tier_is_root_order_independent is real: on the old per-root loop with order [R1=parent,R2=kid] it returned parent. test_hook_bare_directory_kid_refused now plants a kid record at os.getpid(), making the refusal deterministic under any runner. Parent ran the file as a live parent from this worktree: 29 passed (was 1 failed,27 passed on the first round).
<!-- THOUGHT:END -->
