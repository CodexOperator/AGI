---
id: experiment:quorum-request-path-built
mint_id: 48855a6f98a24097a72fa86b7fc71d40
type: experiment
parents:
  - hypothesis:l3w4-quorum-request-path
next_edges: []
confidence: 0.9
edited_by: ubuntu
evidence_runs:
  - experiment:quorum-request-path-built
scaffold_hash: ec2dece8d03b467e
season: 2
title: Quorum request path built directly by the quorum seat, not dispatched
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:quorum-request-path-built

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
Built directly by the quorum seat (alive), not dispatched to a kid -- urgency (master-sensei blocked live, no way to reach the quorum) plus already holding full context from an adjacent branching-issue review made hand-building cheaper than briefing a fresh agent. Change: send.py gains audience_quorum() (posts [ask] into room quorum-requests, open to any caller) and generalizes report() to accept --room in addition to --to (reply posted back into the same room as [report ref=TS], gated to AGI_ROLE=parent + AGI_LADDER_TIER=3 specifically for QUORUM_REQUEST_ROOM -- an ordinary room stays ungated). Also fixed a same-session regression in send.py send --room/--to: the L3.43 harvest reordered target-before-text to fix plain inbox send, which broke --room/--to whenever text arrives as one argv token (target greedily swallowed it). Replaced the two-positional nargs pair with one bucket split explicitly by mode in code. Evidence: 8 new tests in test_send.py (3 for the request path, 2 pinning the regression, 3 gate/scope checks), full suite 2152 passed / 1 skipped, committed+pushed 42355982b.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
owner ruling (relayed by prime, 2026-09-08): quorum room is closed to everyone but the three vision seats; the rest must request a quorum response, and that path did not exist in code (send.py audience only accepted target=prime). Built the door: audience quorum (ask, ungated) + report --room (answer, gated). Found and fixed a live regression in the same file while testing it.
<!-- THOUGHT:END -->
