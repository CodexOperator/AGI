---
id: experiment:a00-4a21983b-capability-probe
mint_id: a004a21983b0f342a000000000000001
type: experiment
parents:
  - hypothesis:a00-4a21983b-0f342a
next_edges: []
loop: hypothesis:a00-4a21983b-0f342a@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
season: 2
title: Fake-provider probe for the single Grok adapter seam
town: core
status: pending
---
# experiment:a00-4a21983b-capability-probe

## Experiment

Add a focused test to `extensions/agi/tests/test_grok_bot_adapter.py` that injects one fake generic pane-capability provider into the existing Grok adapter namespace, then:

1. delegates `pane_attach`, `pane_send`, and `pane_read` through that provider;
2. confirms the required adapter surface still loads unchanged;
3. asserts a named immediate error when the provider is absent;
4. asserts a named immediate error when the provider has no named pane;
5. leaves the existing zero-Grok-hits dispatch assertion intact.

No production implementation is part of this experiment: first observe the expected failure, then let the owning implementation turn the test green. Messaging semantics and hold creation are deliberately absent.

## Result

Pending execution. The current live adapter and focused tests contain no pane methods, so this experiment has not yet measured the generic capability seam.

## Falsifier

The seam is viable only if the fake provider can be injected without a `grok` branch in dispatch/rotate or a second adapter module, and both missing-provider and missing-pane paths fail by name immediately.
