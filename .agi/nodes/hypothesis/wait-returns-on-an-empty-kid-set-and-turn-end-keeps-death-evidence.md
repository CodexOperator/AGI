---
id: hypothesis:wait-returns-on-an-empty-kid-set-and-turn-end-keeps-death-evidence
mint_id: 8763bac015084347908a7b0b3635a49f
type: hypothesis
parents:
  - goal:g15.27.4
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: e374da1d5606f67a
season: 2
testable_claim: After the fix, cli.py cmd_wait returns at once (a named non-zero code) when no agent row matches instead of polling to the deadline, and its heartbeat prints each agent's elapsed time as its docstring promises (cli.py ~2336-2362); and the turn-end reap in dispatch.py and heal.py no longer overwrites a death.evidence that _death_class already set to the stream error; each proved by a committed test red on the pre-fix bytes, with test_cli*.py, test_heal_watch.py and test_dispatch.py green.
title: "A parent's wait and a turn-end keep their evidence (FR-C1, 0921 engine slice; assigned: director-engine)"
town: core
---
# hypothesis:wait-returns-on-an-empty-kid-set-and-turn-end-keeps-death-evidence

# hypothesis:wait-returns-on-an-empty-kid-set-and-turn-end-keeps-death-evidence

## Hypothesis

After the fix, cli.py cmd_wait returns at once (a named non-zero code) when no agent row matches instead of polling to the deadline, and its heartbeat prints each agent's elapsed time as its docstring promises (cli.py ~2336-2362); and the turn-end reap in dispatch.py and heal.py no longer overwrites a death.evidence that _death_class already set to the stream error; each proved by a committed test red on the pre-fix bytes, with test_cli*.py, test_heal_watch.py and test_dispatch.py green.

## Agent Notes
assigned: director-engine (0921 residue batch, engine slice leaf goal:g15.27.4); bytes verified by director-engine 10:3xZ 09-23 before minting.
