---
id: "outcome:a00-ddbe3410-outcome001-chain-bootstrap"
mint_id: 99987248ee034aebb077e7ed5e1b26c5
next_edges:
  - bigger_outcome:a00-ddbe3410-bo001-chain-bootstrap
parents:
  - mvp:a00-ddbe3410-mvp001-chain-bootstrap
tags:
  - bootstrap
  - chain-block
title: "OUTCOME001: task→experiment conversion is feasible"
type: outcome
---

## Input
Pending task node (e.g., `task:t-001` with full acceptance criteria).

## Output
- `nodes/experiment/` file created
- Code implemented in `src/`
- Tests written in `tests/`
- pytest passes
- `nodes/verdict/` file created with PROVED verdict

## Behavior
1. Read task acceptance criteria from `nodes/task/{id}.md`
2. Create experiment node file in `nodes/experiment/`
3. Implement code per acceptance criteria
4. Write tests
5. Run pytest
6. Create verdict node with status=proved

## Edge Cases
- Task with blocked_by: create experiment for blocking task first
- Task with no acceptance criteria: cannot convert (disproved case)
- Implementation fails tests: verdict disproved
