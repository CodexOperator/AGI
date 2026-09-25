---
id: hypothesis:a00-ec8dd0d3-b4a32e
mint_id: c2a2709da1314d49abb72663546c9e42
type: hypothesis
parents:
  - goal:g7.31.1.2.2
next_edges: []
confidence: 0.3
edited_by: a00-ec8dd0d3
evidence_runs:
  - hypothesis:a00-ec8dd0d3-b4a32e
loop: goal:g7.31.1.2.2@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 1ed4a8fadcc4a589
season: 2
testable_claim: "Persistent dispatch rows must survive a killed process by reattaching to the same named tmux pane identity, rather than starting an anonymous replacement. The claim is narrowly about the restart seam: `dispatch.py`'s restart path must use the persisted `pane_id`/named-pane hold adapter, preserve `adapter=tmux_hold`, and set `created=false` on reattach (never claiming a new pane was created). A fake end-to-end test that kills the first launch, exercises restart, and observes the same pane id with anonymous `Popen` forbidden would prove this claim. A restart that creates a new session, loses the pane id, or reports `created=true` would disprove it."
title: Persistent restart reattaches the named pane
town: core
verdict: pending
---
<!-- BODY:BEGIN -->
# hypothesis:a00-ec8dd0d3-b4a32e

## Hypothesis

Persistent dispatch rows must survive a killed process by reattaching to the same named tmux pane identity, rather than starting an anonymous replacement. The claim is narrowly about the restart seam: `dispatch.py`'s restart path must use the persisted `pane_id`/named-pane hold adapter, preserve `adapter=tmux_hold`, and set `created=false` on reattach (never claiming a new pane was created). A fake end-to-end test that kills the first launch, exercises restart, and observes the same pane id with anonymous `Popen` forbidden would prove this claim. A restart that creates a new session, loses the pane id, or reports `created=true` would disprove it.

This extends the existing first-spawn probe rather than repeating it; the unresolved risk is specifically identity across the process-death boundary.
<!-- BODY:END -->

## Agent Notes
Scoped restart/reattach identity hypothesis; no restart probe was run in this round.
