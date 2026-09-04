---
id: experiment:a01-1fc29280-9fd631
mint_id: bfdb217a2e724687bd6f3decc62ef23d
type: experiment
parents:
  - hypothesis:a00-711c2d0f-15bc43
next_edges: []
confidence: 0.0
scaffold_hash: 52dbd7784dab6574
title: A01 1fc29280 9fd631
verdict: pending
---
# experiment:a01-1fc29280-9fd631

## Experiment

**Protocol — controlled comparison (chat vs briefing) across agent dispatches.**

**Design:** Two-condition between-subjects. Each trial dispatches one agent from
the existing `dispatch.py` pipeline to a pre-selected low-complexity build node.
The agent receives either:
- **Chat condition**: the node's version payload + the verbatim agent-logged chat
  from the version that produced it (from `refs/grid/session/*` or grid-inlined
  logs)
- **Briefing condition**: the node's version payload + the node's `THOUGHT` block
  as a post-hoc summary

**Dependent variable:** tool calls before the agent's first *useful action* —
defined as a non-trivial edit to the node payload (not a `read`, `ls`, or dry
run). Scored by `evidence_gate.py` against the node's contract.

**Controls:**
- Same node, same dispatch config, same model per matched pair
- Briefing padded to chat token length with irrelevant filler (third arm if
  practical)
- 10 trials per condition to reach statistical power

**Run command (future):**
```
python3 extensions/agi/bin/dispatch.py --node <build-node-id> \
  --condition {chat|briefing} --count 10 \
  --measure-tool-calls --judge evidence_gate.py
```

**What happened in this session:** Designed protocol only. Full execution
requires agent dispatch budget, which was not allocated for this iteration.
The prior sibling experiment `experiment:a00-af93633e-fea9ca` (same parent
hypothesis) is also unfilled — this hypothesis awaits a dedicated run.

## Evidence

No execution evidence collected in this session. Protocol above is the
artifact. The two sibling scaffolds (`experiment:a00-af93633e-fea9ca` and
`experiment:a01-1fc29280-9fd631`) under `hypothesis:a00-711c2d0f-15bc43`
both remain pending — the hypothesis is correctly scoped for a dedicated
agent-dispatch run, not a single-iteration fill.


## Agent Notes
Designed chat-vs-briefing experiment protocol for G10.1 falsifier. Full execution requires agent dispatch budget across 10+ trials per condition. Both sibling experiment scaffolds under this hypothesis remain pending.
