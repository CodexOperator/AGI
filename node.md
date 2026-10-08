---
id: hypothesis:one-mint-id-assigner-every-writer-imports
mint_id: c3c88aea8aa6420ebd9fefec9b582386
type: hypothesis
parents:
  - goal:g7.16.1.1.4
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: 9a2b7e3665cbba63
season: 2
tags:
  - council-loop
  - bundle-1
  - row-d
testable_claim: (1) ensure_mint_id lives in graph_core.identity and the 4 assign sites become 1 (2) a valid id is never replaced (3) goal:g4.18.1 carries a Falsifier whose output is on the node and each child is complete, parked or gap-only
title: "Assign-a-mint-id-if-missing is ONE function in graph_core.identity that node_writer, snapshot-goals and backfill import; g4.18.1 gains and runs its falsifier (row D; assigned: director-general-3)"
town: core
---
# hypothesis:one-mint-id-assigner-every-writer-imports

## Measured
- The id generator is already one function: `graph_core.identity.mint_permanent_id`, imported by node_writer.py, snapshot-goals.py and backfill-mint-ids.py.
- ASSIGN-IF-MISSING lives in 4 places (`git grep -nE "\[.mint_id.\] *= *mint|new_fm\[.mint_id.\] *=|\"mint_id\": *mint_permanent_id" -- extensions/agi/bin` = 4 lines at 10:2xZ 09-29): node_writer.py create frontmatter (`"mint_id": mint_permanent_id()`) · node_writer.py `adopt` (`fm["mint_id"] = mint`) · snapshot-goals.py `ensure_mint_id` (re-exported by snapshot-build-site.py) · backfill-mint-ids.py main loop (`new_fm["mint_id"] = new_id`).
- goal:g4.18.1 has no `## Falsifier` section.

## CLAIM
(1) ONE function, `ensure_mint_id(fm) -> fm` (never overwrites a valid id, warns on a malformed one), lives in `graph_core.identity`. node_writer create + adopt, snapshot-goals.py and backfill-mint-ids.py import it, and the other three copies are gone. (2) goal:g4.18.1 carries a `## Falsifier` in the [goal] body order, and its output is pasted on the node. Each g4.18.1.N is then complete, parked, or narrowed to its measured gap.

## Dispatch line
config-max: none (identity is code). template-max: g4.18.1's falsifier is a goal-body edit through write.py, not code. code: moving the ONE existing `ensure_mint_id` into graph_core.identity and routing 3 call sites through it -- the resolver exists, so no new logic.

## FALSIFIERS
- The Measured grep prints more than 1 line after the round.
- A node that already carries a valid mint_id gets a new one from any path (goal:g2.5).
- `snapshot-goals.py --render --check` is not byte-identical afterwards.

## TESTS
extensions/agi/tests/test_snapshot_build_site.py (the ensure_mint_id rows) + a new row + `test_bin_help_smoke.py`, `--basetemp /tmp/b1d`; a pinned row: an fm with a valid id is returned unchanged.

## FILE SCOPE
extensions/agi/src/graph_core/identity.py · extensions/agi/bin/node_writer.py · extensions/agi/bin/snapshot-goals.py · extensions/agi/bin/backfill-mint-ids.py · their tests · goal:g4.18.1 and its children (through write.py)

## CEILING
no dispatch (goal:g7.16.1: director-general-3 builds directly) · net production lines <= 0 (a consolidation removes lines) · <= 20 test lines · 0 USD
