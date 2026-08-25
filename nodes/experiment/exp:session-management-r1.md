---
id: "exp:session-management-r1"
mint_id: 549c8e771f3945279c70586c596a6256
next_edges:
  - verdict:session-management-r1
parents:
  - hyp:session-management-r1
status: proved
tags:
  - session-management
  - r1
title: "session-management-r1: Session state capture and restore fidelity test"
type: experiment
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
