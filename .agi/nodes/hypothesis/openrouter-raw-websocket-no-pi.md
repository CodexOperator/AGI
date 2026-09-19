---
id: hypothesis:openrouter-raw-websocket-no-pi
mint_id: 3ed902787bc24d4ea154e3f13872cfb8
type: hypothesis
falsifier: "Model call still shells out to pi for inference, or Claude aliases bill on OpenRouter, or landing skips idea→hypothesis→experiment."
testable_claim: "A director can complete one parent turn via unified dispatch/workflows where the model call uses a raw OpenRouter websocket or SSE client (no pi CLI for inference), attributes spend to OPENROUTER_API_KEY or a minted key, and mints/edits a child graph node without crossing Claude subscription aliases into the OpenRouter namespace."
parents:
  - goal:g4.3
next_edges: []
confidence: 0.4
edited_by: owner
link_ref: /tmp/agi-payloads/openrouter-raw-ws-hyp.md
location: source_root
scaffold_hash: 3e600af35ce5a756
season: 2
spawn_gate: bypassed
status: active
thought_session: grok-bot-season2-migrate
title: Raw OpenRouter websocket / non-pi inference path for unified dispatch
town: streaming-suite
---
<!-- BODY:BEGIN -->
# CLAIM
A director can grow the chain (idea→hypothesis→experiment) by dispatching pi parents whose **model calls** ride a **raw OpenRouter WebSocket / streaming HTTP path** that does **not** require the pi CLI as the inference transport — i.e. unified dispatch/workflows still orchestrate parents on pi boxes, but the token stream itself is a raw OpenRouter socket (or OpenRouter-compatible SSE/WS) so non-pi harness adapters (including grok-bot) can share one spend rail.

This extends `goal:g4.3` clause 4 (raw-API harness) and learns from `hypothesis:ws-raw-zero-injection-adapter` (local llama WS relay) without conflating local llama with OpenRouter cloud.

## TESTABLE CLAIM (director-owned round)
1. A workflow stage declared in config can target provider=openrouter with transport=raw_ws (or raw_sse) and complete one parent turn that mints or edits a child hypothesis node.
2. The path does not import or shell-out to the pi binary for the model call (pi may still host the parent process / tools).
3. OPENROUTER_API_KEY (or a minted per-spawn key) is the only credential; no Claude subscription alias crosses into the OpenRouter namespace (`hypothesis:l3-workflow-model-crosses-harness-namespace`).
4. Suite-safe: one new adapter module + tests; no orphan build nodes; parents stay on OpenRouter spend rail.

## FALSIFIERS
- Model call still requires `pi` CLI for inference → claim fails.
- Any Claude subscription alias billed on OpenRouter → namespace bug; stop.
- Full websocket stack lands without idea→hypothesis→experiment parents → process violation.

## DIRECTOR BRIEF
See `doc:director-brief-openrouter-raw-ws`. Run via unified dispatch/workflows on pi parents. Do **not** implement the full stack in the first round unless suite-green and small; prioritize graph scaffolding + measured probe.

## FILE SCOPE (suggested)
- New: adapter stub + tests under extensions/agi (director names exact paths in experiment)
- Touch: workflow config cells only via write.py
- Never: season2/main MAIN tip; never seat parents on Grok
