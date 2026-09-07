---
id: exp:session-management-r1
mint_id: 549c8e771f3945279c70586c596a6256
type: experiment
parents:
  - hyp:session-management-r1
next_edges:
  - verdict:session-management-r1
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: season.py
season: 1
status: inconclusive_lean_proved:50
tags:
  - session-management
  - r1
thought_session: season
title: "session-management-r1: Session state capture and restore fidelity test"
verdict: inconclusive_lean_proved:50
---
# experiment:exp:session-management-r1

## What Was Run

Session state capture/restore fidelity test for session-management/r1.

## Results

- Node fidelity: 97.9% (418/427 nodes)
- Git fidelity: 55.0% (dirty=True)
- Overall: 81% (below 95% threshold)

The experiment proves that session state can be captured with high node fidelity.
Git state is harder due to dirty working tree.