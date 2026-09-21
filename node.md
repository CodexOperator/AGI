---
id: hyp:a00-204c9d9e-1d958f
mint_id: af73b11909574cecb20fb332b76f3688
type: hypothesis
parents: []
next_edges:
  - exp:exp:a00-204c9d9e-1d958f
domain: domain-query-api
edited_by: season.py
season: 1
status: pending
tags:
  - architecture
  - query-api
  - capillary-dag
  - task-prioritization
thought_session: season
title: Query API enables rational task selection in the capillary DAG
---
# hyp:a00-204c9d9e-1d958f

## Hypothesis

**Claim**: A Query API wrapping the capillary DAG graph loader can answer strategic navigation questions that enable agents to select high-value tasks — reducing the current 90-task blind spot and accelerating chain completion.

**Current gap**: 90 pending tasks, 0 task-priority queries. Agents extend longest chains or pick randomly. No API surfaces which tasks are (a) closest to completing a domain chain, (b) unblocking multiple downstream hypotheses, or (c) on under-explored domains.

**Query API surface** (functional requirements):
1. `task_attractiveness(task_id)` → score based on descendant_count, chain_recency, type_balance
2. `chain_gaps(domain)` → list of hypothesis nodes in a domain with no verdict yet, sorted by urgency
3. `next_best_hypothesis(attractiveness_fn)` → top-N hypotheses to extend next
4. `coverage_report()` → per-domain counts: ideas/hypotheses/experiments/verdicts/MVPs/outcomes

**Testable claim**: The Query API correctly computes all 4 queries against the live 157-node graph (90 tasks, 60 hypotheses, 7 ideas).

**Prove it**: Implement the Query API in `query_api/` module, run pytest asserting each query returns non-empty results matching known graph state.
**Disproves it**: Any query returns empty results for a domain that has known non-empty state, OR the API crashes on the 157-node graph.

**Why this matters**: The capillary DAG needs an agent-facing "brain interface." Without strategic task selection, parallel agents will duplicate work or leave domain gaps. The Query API closes the loop between graph state and agent decision-making.