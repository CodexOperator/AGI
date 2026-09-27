---
id: goal:g4.20.1
mint_id: 670cfcc3e2384c35b7f66b2788bf54bf
type: goal
parents:
  - goal:g4.20
next_edges: []
confidence: 0.7
edited_by: belam
goal_id: G4.20.1
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 2b337790deb901f0
season: 2
seeds: []
status: active
tags:
  - engine
  - harness
  - elegance
title: "G4.20.1: ONE HARNESS SOURCE -- one .geometry catalog names every harness and the default (bare pi = the free lane, paid = pi-paid by explicit flag only); routes name a harness, never a model; eleven setting places become three (assigned: director-engine)"
town: core
---
# goal:g4.20.1

# goal:g4.20.1

## OWNER 2026-09-27 15:3xZ (belam's pane), verbatim
"Also can we simplify how many places harnesses are set? The separate config.json could be moved into .geometry to unify it with the rest but it just feels like there's too many places. Like the fallback in workflow seems unneeded, and the default pi harness should already be pi free. Just feels like 8 places is excessive. I know to config and template max but couldn't some be unified?"

## Why this exists
goal:g4.20 (everything is a node, configs included): the config.json `harnesses` block is a config with no node. On 2026-09-27 the account drained (192 USD bought, 0.606 left) because ONE of the places that name a harness still said the paid `pi` after the ladder moved to `pi-free` -- config:workflows default + type rows (thought-master [red] 06:42Z, ~12.8 USD of murs). Measured by the Prime 15:3xZ, a harness or model is set in ELEVEN places: (1) .agi/config.json harnesses.* (the catalog, a model per role) (2) config.json spawn.harness (3) config.json agent_dispatch.provider/model (adapters/__init__.py:222 synthesizes a hidden paid-deepseek harness from it) (4) config.json workflows.<name>.provider/model (5) workflow manifest provider (6) config:workflows workflows[].harness (7) config:workflows types[].harness (8) config:workflows default_harness (9) config:ladder rows harness AND model (the model a second time) (10) config:posts rows harness + model (11) --harness / AGI_HARNESS at run time. workflow.py resolves through five levels (config row, manifest, per-workflow, type, prime default; workflow.py:345-374).

## Target end-state
- ONE catalog node under .agi/nodes/.geometry/ (the config.json `harnesses` block moves there): each harness = adapter, bin, model per role, and `paid: true` only on a paid one; ONE `default` cell in it.
- The bare name `pi` IS the free lane (today's pi-free); the paid lane is named `pi-paid` and is reachable only by an explicit --harness (plus thought-master's explicit-ask guard while the default lane is zero_usd).
- Routing names a harness, never a model: the ladder keeps its harness column and drops its model column (the model comes from the catalog); config:workflows keeps `types[].harness` ONLY for a type that deviates from the default (trove-survey -> claude-code).
- Deleted: spawn.harness, agent_dispatch (and its synthesized legacy harness), config.json workflows.*.provider/model, manifest-level provider, config:workflows workflows[].harness and default_harness. Workflow resolution = --harness > type row > catalog default: three levels, one code path shared with dispatch.
- config:posts seat rows keep their identity cells (a live seat's harness + model are facts about that seat, written by rotate).

## Invariants
- No bare or defaulted resolution ever lands on a paid harness.
- Every harness a route names exists in the catalog; an unknown name refuses by name, never falls back.
- Rows are retired or moved, never deleted (the deprecated/ rule); config.json keeps only non-harness tuning.

## Falsifier
1. `git grep -nE '"(provider|harness|default_harness)"' -- .agi/config.json extensions/agi/workflows/*.json` = 0 hits, and `git grep -n agent_dispatch -- extensions/agi/bin` = 0 live readers; `workflow.py list` and a `dispatch.py --dry-run` per ladder row both print the harness the catalog default or the one deviating type row names.
2. Negative: a test resolves every workflow and every ladder row with no --harness and asserts none has `paid: true`; a manifest or config row that re-adds a provider fails the suite.

## Out of scope
goal:g7.32.6 (messaging) · the zero-usd mint floor fix (belam [decision] to director-engine 13:1xZ, lands FIRST: resume before redesign) · goal:g4.18.1 (the mint route).

## Agent Notes
Assigned to **director-engine**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam-S2-L5-XIII 15:3xZ 09-27: minted on the OWNER 15:3xZ question (verbatim in the body). Nested under goal:g4.20 (everything is a node) rather than a new G4 sibling: the config.json harnesses block is exactly a config without a node, and the skill rule is nest rather than widen. Eleven places measured from the resolvers (workflow.py:345-374, adapters/__init__.py:222, dispatch.py:2113, config:ladder, config:workflows, config.json), not from the owner eight. Queued BEHIND the zero-usd mint fix (resume first).
<!-- THOUGHT:END -->
