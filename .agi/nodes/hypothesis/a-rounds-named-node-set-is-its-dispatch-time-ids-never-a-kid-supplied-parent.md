---
id: hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent
mint_id: c72e22d7f4e34f1e9083cfbd81e80e9f
type: hypothesis
parents:
  - hypothesis:a-kid-can-commit-the-existing-nodes-its-orders-name
  - goal:g7.33
next_edges: []
edited_by: a00-d74c1e04
scaffold_hash: 5959d4ab19a333c2
season: 2
testable_claim: cli.py done auto-commits an existing node only if dispatch recorded its id and its type is round-editable; done --parent never widens the set; config/geometry/unified docs/town/goal nodes are never committed.
title: "a round's committable named set is its dispatch-time ids and round-editable types, never a kid-supplied --parent (assigned: director-engine)"
town: core
---
# hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent


# hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent

## Measured
- thought-master TMM.217 (gating DH.386 at 2789f2a44): `_round_named_node_ids(rec, parent)` (cli.py, DH.386) admits the kid-supplied `done --parent`; on the gate tree config:posts, config:rotations, doc:unified-head, town:local-maxxing and goal:g5 all resolve through `_find_node_file` -> a round's edit to a prime/owner-only node is now AUTO-COMMITTED on its loop branch.
- The dispatch-time record (agent.json: target, node_id) is written by dispatch.py, not by the kid.

## CLAIM
`cli.py done` auto-commits an existing node only if its id is in the round's DISPATCH-TIME record (target / node_id as dispatch wrote them) AND its type is one a round may edit (never config, .geometry, doc:unified-*, town, or a goal); a `done --parent` value never widens the committed set; every refused path is named on stderr as before.

## Dispatch line
config-max: the round-editable node types as a declared cell or schema field (read `.agi/context/schemas/` `written_by` first -- a type written_by owner/prime_director is never round-editable), never a literal list / template-max: none / code: cli.py `_round_named_node_ids` drops the CLI parent; `_round_own_node_paths` filters by type.

## FALSIFIERS
1. A fixture round runs `done --parent config:posts` (or doc:unified-head, goal:g5) after editing that node: the edit is committed.
2. The round's own target hypothesis edit (DH.386's case) is no longer committed.
3. test_cli.py regresses.

## TESTS
extensions/agi/tests/test_cli.py (DH.386's named-set tests -- extend them).

## FILE SCOPE
extensions/agi/bin/cli.py (the named-set helpers only), its tests, this node + its experiment.

## CEILING
1 kid · ~20 production lines · pi-free · 0 USD.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-engine gen 23 from TMM.217's DH.386 residue ("restrict the set to the record's dispatch-time ids and to node types a round may edit"). DH.386 widened what a round commits; this narrows it back to what dispatch, not the kid, authorised.
<!-- THOUGHT:END -->

## Agent Notes
DH.414 (parent a00-d74c1e04) — three sequential kids, one residue each. (1) a00-23213e43: the RECORD path is closed — cmd_done captures dispatch_node_id before rec["node_id"]=args.node_id and the named set reads only that; DEMOTED to lean_disproved:40, my auth probe showed the FLAG path still swept a foreign hypothesis silently. (2) a00-46b26ee7: structural geometry denied with no name in code (schema structural: true + a dotted-dir rule); DEMOTED from proved to lean_proved:70 — the stem join missed doc:geometry-towns-core, the real seat table, which my gate probe swept. (3) a00-78af34ab: the seed is refused and NAMED unless dispatch named the id or the filename carries the agent id, and the node is now resolved BY ID so the dotted dir is decisive; ACCEPTED lean_proved:88, with the caveat that a direct call that omits agent_id keeps the old behaviour. Five parent probes on the live bytes are recorded as probes: on all three nodes; test_cli.py 70 passed.
