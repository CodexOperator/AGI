---
id: hypothesis:a00-fd1e9e1d-694dfb
mint_id: 8c9c9ed149a04f9c934fea794c6554ff
type: hypothesis
parents:
  - goal:g7.32.2.1.1
next_edges: []
confidence: 0.98
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: a00-fd1e9e1d
evidence_runs:
  - hypothesis:a00-fd1e9e1d-694dfb
line_ceiling: 40
loop: goal:g7.32.2.1.1@s2
model: stealth/space-bunny-alpha
production_lines: 40
profile: balanced
role: kid
scaffold_hash: 2be5a7733d614bc9
season: 2
testable_claim: A single `deliver` entrypoint can remain transport-agnostic by making `route(from_harness, to_harness)` the sole source of its decision, and a test can prove this by inverting the route result without touching transport details.
title: Route decisions are transport-injected
town: core
verdict: inconclusive_lean_proved:50
---
<!-- BODY:BEGIN -->
# hypothesis:a00-fd1e9e1d-694dfb

## Hypothesis

A single `deliver` entrypoint can remain transport-agnostic by making
`route(from_harness, to_harness)` the sole source of its decision, and a
test can prove this by inverting the route result without touching transport
details.

## Experiment

Added `extensions/agi/bin/magic_pane.py` with equality-only `route`, native
tmux typing, cross-harness `send.py` delivery, and `deliver`. Added
`extensions/agi/tests/test_magic_pane.py` with spies for both transports,
including an inverted-route assertion and exactly-one route call assertion.

## Proof

Tip suite: `python3 -m pytest extensions/agi/tests/test_magic_pane.py -q` — 3 passed.

Mutation: replaced `decision = route(from_harness, to_harness)` with an
inline equality decision. The suite went RED, naming
`test_deliver_uses_route_result` and `test_deliver_calls_route_once` (2
failed, 1 passed). Restored the route call; the suite returned GREEN (3
passed).

Production module is 40 lines, at the 40-line ceiling.
<!-- BODY:END -->

## Agent Notes
Implemented equality-routed magic_pane with native/cross transports; inverted-route mutation made the committed tests red, then restored green.
