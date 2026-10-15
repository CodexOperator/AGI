---
id: hypothesis:l5-rotate-wires-apply-staged-into-the-rotation-boundary
mint_id: 4da17948e2cc4b1f9e8c165deacc7a7f
type: hypothesis
parents:
  - goal:g1.20
next_edges: []
confidence: 0.7
edited_by: belam
scaffold_hash: 6170294ef834a312
season: 2
testable_claim: "rotate.py wires the already-defined-but-never-called _apply_staged (line 3898) into the rotation boundary: rotate/rotate-self reads seats/<old>.rename.json BEFORE the successor spawn, re-derives every surface from branches.py + the row at that moment (the json is a plan, refused on drift, never trusted stale), applies atomically (SM.18's function), seats the successor under the NEW name (window, --remote-control name, worktree dir, post branch, row + session_label, key/ack/bootstrap files, inbox + nudge files, dm logs + sidecars, alerts edges), writes the applied surfaces into the rotation record, and consumes the json; refuses cleanly on a dirty tree; a missing view session (no livestream) is never treated as a red. Fixture-proven with a fake tmux, no live pane."
thought_session: dissolve-legacy-2026-09-19
title: L5 rotate wires apply staged into the rotation boundary
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-rotate-wires-apply-staged-into-the-rotation-boundary

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
