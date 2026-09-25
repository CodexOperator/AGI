---
id: verdict:a00-4a0e4ba2-4cc1ff
mint_id: 737a50c666144a8e825efa54cdfffa6c
type: verdict
parents:
  - experiment:a00-6858a2d4-d5e9be
next_edges: []
confidence: 0.92
edited_by: a00-4a0e4ba2
evidence_runs:
  - experiment:a00-6858a2d4-d5e9be
loop: experiment:a00-6858a2d4-d5e9be@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 708785d04177cc3c
season: 2
title: First-spawn wiring contract proved
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# verdict:a00-4a0e4ba2-4cc1ff

## Verdict

**proved** — the narrow first-spawn wiring claim is established for the
experiment's stated scope.

## Evidence

The cited run, `experiment:a00-6858a2d4-d5e9be`, reports a production
`dispatch.py` `_open_round` that calls `tmux_hold.start_or_popen` with the
computed child environment, cwd, log, mode, seat, agent id, and per-agent
state directory, and has no direct `Popen` in that nested function. The
strengthened AST assertion checks those required keywords, rather than only
the method name. The focused held-pane suite passed 3 tests, including
first-launch session/pid/spec behavior, pane preservation on restart, and
the direct-Popen fallback with environment forwarding when tmux is
unavailable.

This verdict deliberately does not claim the broader cleanup behavior:
partial-new-session cleanup, hold.json lifecycle deletion, and the
production rc=0 regression remain outside the experiment.

## Confidence

0.92

## Agent Notes
Proved the narrow first-spawn wiring contract with keyword-level AST assertions and three passing held-pane tests; broader cleanup lifecycle remains open.
