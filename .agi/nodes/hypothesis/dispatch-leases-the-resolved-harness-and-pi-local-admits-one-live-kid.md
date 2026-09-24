---
id: hypothesis:dispatch-leases-the-resolved-harness-and-pi-local-admits-one-live-kid
mint_id: ca0a52fe4c074ddc8fbd76c565a74d53
type: hypothesis
parents:
  - goal:g5.27
next_edges: []
edited_by: director-engine
scaffold_hash: c93ff4a5404f592d
season: 2
testable_claim: With pi-local max_live 1 and a live pi-local lease, dispatch.main() --harness pi-local never calls Popen and records the slot in manifest.unadmitted.
title: dispatch passes its resolved harness into the lease, and with pi-local max_live 1 a second live pi-local spawn is unadmitted (leaf 2/2 of TMM.82)
town: local-maxxing
---
# hypothesis:dispatch-leases-the-resolved-harness-and-pi-local-admits-one-live-kid

## Measured
- dispatch.py:2335-2336 -- the one live admission call `spawn_budget.acquire(root, cap, agent_id, tier=args.tier, iter_n=...)`
  passes no harness; the refusal path :2357-2370 (stderr `unadmitted <id> slot=<n>: spawn budget full ...`, manifest reason), exit
  0 at :3041 -- all before --branch cuts a worktree (:2393).
- harness_name resolves at :1947-1999; the agent record's harness (:2843/:2853) is written only after commit (:2830) -- too late.
- test_adapters.py:192-203 bans `harness == ` in dispatch.py; a kwarg `harness=harness_name` does not trip it.
## CLAIM
dispatch passes `harness=harness_name` into acquire; with `"max_live": 1` on the pi-local row (.agi/config.json 64-77), a second
live pi-local spawn becomes a NAMED unadmitted slot; other harnesses still admit up to spawn.max_live.
## Dispatch line
config-max: .agi/config.json harnesses.pi-local "max_live": 1 / template-max: none / code: dispatch.py main(), one kwarg at :2336
## FALSIFIERS
- Popen is called for the refused slot, or a --harness pi spawn is refused
- test_adapters.py, test_credential_none_spawn.py or test_dispatch_dry_run.py red
## TESTS
test_credential_none_spawn.py::test_a_second_pi_local_spawn_is_unadmitted_at_the_row_max_live -- the `project` fixture's config
(:65-92) with pi-local max_live 1; an occupant lease (acquire harness="pi-local", commit os.getpid(), as test_dispatch.py:571-573);
`_stub_popen` (:95-119), `_argv(project, "pi-local")`: main() == 0, no argv captured, one manifest.unadmitted entry, stderr names
pi-local. Red today (admitted). Neighbours: test_adapters.py, test_dispatch.py, test_dispatch_dry_run.py.
## FILE SCOPE
extensions/agi/bin/dispatch.py 2331-2370
extensions/agi/tests/test_credential_none_spawn.py 55-131 (+ the new test appended after the file's last test; the file ends at 342)
.agi/config.json 64-77
## CEILING
1 kid (--harness pi-free) · 1 production line + 1 config cell · 0 USD · SECOND (after the acquire leaf merges)
RESIDUE: a --harness pi round with PI_CODING_AGENT_DIR reaches the same local slot and a row-keyed cap cannot see it; leases taken
before landing carry no harness; restart leases (:3590-3592) carry none (dormant while reaper.max_restarts = 0).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The config half was added by the director (04:2xZ 09-24): .agi/config.json harnesses.pi-local gains max_live 1, the cell this node's Dispatch line names. Two kid rounds missed it -- EF.99's kid died on a provider 401 before any bytes, and EF.100 committed only the test (its fixture builds its own tmp config) -- and under TMM.94 (minimal token use) a third round for one JSON value was the wrong trade. Code half = EF.97's kwarg, test = EF.100's; the director measured red before the kwarg and green after (282 passed), and with the real config in a tmp root the first pi-local acquire is admitted, the second refused by name at (1/1), and pi-free still admitted.
<!-- THOUGHT:END -->
