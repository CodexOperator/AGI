---
id: hypothesis:a00-b5e2d5be-fddaa2
mint_id: 492b29c69ec44a80992a23aef8b21d14
type: hypothesis
parents:
  - goal:g7.31.1.2.2
next_edges: []
confidence: 0.99
edited_by: a00-b5e2d5be
evidence_runs:
  - experiment:a00-dispatch-hold-probe
loop: goal:g7.31.1.2.2@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: aac3f0ee4454668b
season: 2
testable_claim: The first dispatch spawn should use the existing `tmux_hold` seam, and the agent record should contain the real launch identity only after that seam returns a successful result.
title: Dispatch hold seam is absent
town: core
verdict: pending
---
<!-- BODY:BEGIN -->
# hypothesis:a00-b5e2d5be-fddaa2

## Hypothesis

The first dispatch spawn should use the existing `tmux_hold` seam, and the
agent record should contain the real launch identity only after that seam
returns a successful result.

## Finding

The claim is false for this checkout. The production `_open_round` at
`extensions/agi/bin/dispatch.py:2651-2661` directly calls `subprocess.Popen`;
there is no `tmux_hold` symbol, pane id, or created status in the spawn path.
The evidence run is `experiment:a00-dispatch-hold-probe`.

## Agent Notes
Probe found no tmux_hold seam: dispatch._open_round directly Popen()s at dispatch.py:2651-2661; no pane identity or created status exists to test.
