---
id: hyp:a00-e07eb43f-0ae7b3
mint_id: 67fb39923f7144ccb382b9ae6506eae0
type: hypothesis
parents: []
next_edges: []
edited_by: season.py
season: 1
thought_session: season
title: A00 e07eb43f 0ae7b3
---
# hyp:a00-e07eb43f-0ae7b3
## Hypothesis

**Claim:** Adding a `task→experiment` transition to the chain-engine enables the dispatcher to auto-spawn experiments from pending tasks, closing the 92-task backlog gap.

**What would prove it:**
- The chain-engine accepts `task` as a valid parent type in `_VALID_TRANSITIONS`
- Dispatcher picks the highest-priority pending task and creates an experiment node with `parents: [task:t-NNN]`
- After execution, verdict is recorded under the experiment
- Chain length grows via task→experiment→verdict hops (not just verdict→experiment→verdict)
- At least one pending task advances to verdict state

**What would disprove it:**
- Task nodes have no canonical `status` or `priority` field to rank them
- Task descriptions lack enough structure for LLM to execute without human interpretation
- The chain-engine's DAG validation rejects tasks as valid chain members (cycle risk or type mismatch)
- 80%+ of task bodies are too vague to auto-generate a meaningful experiment script

**Test:** Add `task→experiment` to `_VALID_TRANSITIONS`, write one experiment from a pending task (e.g., t-001), verify chain grows by 1 hop and verdict is recorded.

**Why this matters:** 92 tasks are stuck at `status: pending`. Every task that never becomes an experiment is a dead end in the DAG. If tasks can feed directly into experiments, the capillary chain grows organically from the work backlog instead of requiring manual hypothesis→experiment authoring for every new idea.