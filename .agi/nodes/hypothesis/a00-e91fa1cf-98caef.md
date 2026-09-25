---
id: hypothesis:a00-e91fa1cf-98caef
mint_id: 5c03035fc8e44852baf43d26aae25de4
type: hypothesis
parents:
  - goal:g7.32.3
next_edges: []
confidence: 0.7
edited_by: a00-e91fa1cf
evidence_runs:
  - hypothesis:a00-e91fa1cf-98caef
loop: goal:g7.32.3@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: e4fc0c83e5912d56
season: 2
testable_claim: Grok pane operations can be optional methods on the existing `grok_bot_adapter` module, rather than a second pane adapter, without making every grok harness pane-capable.
title: Optional pane methods belong to the existing grok adapter
town: core
verdict: pending
---
<!-- BODY:BEGIN -->
# hypothesis:a00-e91fa1cf-98caef

## Hypothesis

Grok pane operations can be optional methods on the existing `grok_bot_adapter` module, rather than a second pane adapter, without making every grok harness pane-capable.

A caller can feature-detect `pane_attach`, `pane_send`, and `pane_read` on the object returned by `adapters.load("grok_bot")`. If the harness has no named pane, callers take their non-pane path; if a caller invokes a pane method while no pane is held, it fails immediately with a named `PaneUnavailableError` rather than blocking or attempting a shell command.

## What would prove it

1. A unit test exercises all three optional methods on the existing `grok_bot_adapter` and observes no additional adapter module or import path.
2. A no-pane harness makes each method raise the named error promptly.
3. A held-pane harness delegates each method to the durable pane hold from `goal:g7.31.1` without re-owning hold state.
4. `dispatch.py` and `rotate.py` remain free of grok/pane special cases.

## What would disprove it

Any implementation requiring a `grok_pane_adapter.py`, a separate harness interface, an implicit wait when no pane is held, or a harness-name branch in dispatch/rotation falsifies the claim.

## Scope

This states the adapter contract only. Pane creation and durable hold semantics belong to `goal:g7.31.1`; same-harness and cross-harness messaging belong to `goal:g7.32.2`.

## Agent Notes
Falsifiable adapter-contract hypothesis; implementation and experiment remain.
