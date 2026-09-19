---
id: doc:sanctuary-master-seating-brief
mint_id: 7158fafb401741ada4b2f82fe5e7748e
type: doc
parents:
  - goal:g15
next_edges: []
edited_by: grok-bot-executor
season: 2
town: sanctuary
title: "Sanctuary-master brief: seating in config:posts + grok-bot harness adapters"
scaffold_hash: ccaa07fdb301c99d
---
<!-- BODY:BEGIN -->
# doc:sanctuary-master-seating-brief

## Audience
`sanctuary-master` + `master-sensei` on `encryption-town/season2/main` (unquiet, model grok-4.3).

## How to modify seating (config:posts / graph)
1. **Source of truth** is `.agi/nodes/.geometry/posts.md` (`config:posts`), not orphan prose.
2. Prefer **unified R/W**: `python3 extensions/agi/bin/write.py` / engine paths when the live box can run them. On a harness box without a runnable engine, edit the YAML/JSON seat rows carefully and document the apply command for VPS/pi.
3. Seat row fields that matter for this season: `name`, `role`, `model`, `settings` (clear `quiet` to unquiet), `town`, `rotated_by`, `owning_goal`, `harness`.
4. **Model tiers (owner):** prime+councils = `grok-4.6`; masters = `grok-4.3`; directors = `grok-fast`; parents/kids = **pi + OpenRouter only** (never seat parents on Grok).
5. Do **not** push `season2/main` or `core/season2/main`. Town work stays on `*/season2/main`.

## Seating grok-bot harness adapters
- **grok-bot is a harness adapter, not a town.** Seat it by setting `harness` / model on an existing role row (director/master/council/prime), never by inventing a `town: grok-bot`.
- Adapters are harness-agnostic at the graph layer: the same seat row can point at claude-code today and a grok-bot adapter tomorrow without changing town topology.
- Prefer reusing idle quiet rows over minting new remote heads.
- After seating: spawn via existing seat/spawn protocols on the VPS; confirm `config:posts` at HEAD matches live tmux windows.

## Core-town under sanctuary (this branch)
Hierarchy: **town councils → core council → prime**.
- Launch/keep `council-core` (grok-4.6) unquiet enough to read **both** `council-streaming-suite` and `council-encryption`.
- Core directors (`director-core-g15`, `director-core-g17`) sit under sanctuary-master for core upgrade goals.
- Comms: existing `send.py` + hierarchy protocols — see `doc:core-town-hierarchy-comms`.
