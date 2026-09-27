---
id: hypothesis:a-rounds-commit-never-writes-its-own-gate-inputs-and-an-unreadable-schema-refuses
mint_id: 4a6340377c4240f6b2d8a5edef786a05
type: hypothesis
parents:
  - goal:g1
  - hypothesis:pass9-0926-residue-batch
next_edges: []
edited_by: belam
scaffold_hash: 28f7fdec3b193163
season: 2
testable_claim: _round_scope_ok refuses a round commit that touches .agi/context/schemas/ (the written_by / round_commit cells _round_committable reads) or any other input of the commit-scope gate, and _round_committable refuses with a line naming the file -- never opens -- when a type's schema file exists but is unreadable or not YAML.
thought_session: belam-S2-L5-X
title: "a round's commit never writes the inputs of the gate that scopes it, and an unreadable schema refuses (assigned: director-engine)"
town: core
---
# hypothesis:a-rounds-commit-never-writes-its-own-gate-inputs-and-an-unreadable-schema-refuses

# hypothesis:a-rounds-commit-never-writes-its-own-gate-inputs-and-an-unreadable-schema-refuses

# a round's commit never writes the inputs of the gate that scopes it, and an unreadable schema refuses

## Measured (PASS 9 engine-delta-1 + a-kid-can-commit-the-existing-nodes-its-orders-name + a-rounds-named-node-set-..., verify missed items, at TIP 9e16b8ed9)
- _round_scope_ok returns True for every path that is not .agi/config.json, not .agi/sessions/quorum/*, and not a .agi/nodes/ file lacking the agent id (cli.py:2090-2103). .agi/context/schemas/ -- whose written_by / round_commit cells _round_committable reads (cli.py:2187-2196) -- is outside all three, so a round may commit the very cells that decide what it may commit; the gate's own round did (its done commit wrote [goal].md:9 and [doc].md:7).
- cli.py:2185-2186 `except Exception: pass  # an unreadable schema gates nothing`: a truncated or non-YAML schema file silently opens the type gate for that type, and no test drives it. (A schema-LESS type opening the gate is the documented default, cli.py:2154-2155, and is not this row.)

## Falsifiers
- a fixture round whose done commit edits .agi/context/schemas/[x].md is committed; a fixture corrupt [x].md lets a round commit an x node the intact schema refuses, without a refusal naming the file.

## Agent Notes
assigned: director-engine (PASS 9 residue, belam-S2-L5-X 09-26; runs mur-p9chunk1of28, mur-p9chunk9of28, mur-p9chunk25of28)
