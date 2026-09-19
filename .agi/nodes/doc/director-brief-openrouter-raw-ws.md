---
id: doc:director-brief-openrouter-raw-ws
mint_id: 15790140ee0044d88ec491cd9ea69cce
type: doc
tags:
  - doc
  - season2
  - streaming-suite
parents:
  - hypothesis:openrouter-raw-websocket-no-pi
  - goal:g4.3
next_edges: []
edited_by: owner
link_ref: /tmp/agi-payloads/director-brief-openrouter-raw-ws.md
location: source_root
scaffold_hash: 3fb90788f919ed6d
season: 2
spawn_gate: bypassed
status: active
thought_session: grok-bot-season2-migrate
title: "Director brief: raw OpenRouter websocket (no pi inference)"
town: streaming-suite
---
<!-- BODY:BEGIN -->
# Director brief — raw OpenRouter websocket / non-pi inference path

**Own:** `hypothesis:openrouter-raw-websocket-no-pi` (parent `goal:g4.3`).
**Read first:** `doc:unified-director-brief`, `goal:g4.3` clause 4, `hypothesis:ws-raw-zero-injection-adapter` (local precedent — do not duplicate llama relay).

## Mission
Grow the chain so a director can run a measured experiment proving OpenRouter tokens can stream over a **raw** websocket/SSE path **without** pi as the inference transport, while parents/kids remain on the OpenRouter spend rail and workflows stay unified.

## First round (scaffold, not full stack)
1. Mint idea (if missing) → refine this hypothesis → one experiment with a probe script.
2. Probe: one streaming completion against OpenRouter using raw HTTP SSE or WS client; assert: (a) tokens arrive, (b) process tree / imports show no `pi` binary for the model call, (c) cost attributes to OPENROUTER_API_KEY / minted key.
3. If probe green: bank adapter interface + config cell design in the experiment node; leave full wiring to a follow-on hypothesis.
4. Merge-up to your master with evidence_runs; do not push MAIN.

## Constraints
- Parents/kids: pi + OpenRouter only (orchestration OK on pi; inference raw).
- Directors: grok-fast; do not seat parents on Grok.
- Suite-safe landings only; no orphan builds.
- Cap spend; fail closed on workspace budget 403.
