---
id: experiment:a01-1fc29280-9fd631
mint_id: bfdb217a2e724687bd6f3decc62ef23d
type: experiment
parents:
  - hypothesis:a00-711c2d0f-15bc43
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 52dbd7784dab6574
season: 1
thought_session: season
title: "G10.1 falsifier protocol: chat-vs-briefing agent dispatch with full tool-call instrumentation"
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

**Run command (illustrative — the flags do not exist in `dispatch.py` today;
the pipeline extension this names is part of the work):**
```
python3 extensions/agi/bin/dispatch.py --node <build-node-id> \
  --condition {chat|briefing} --count 10 \
  --measure-tool-calls --judge evidence_gate.py
```

**What happened in this session:** Designed protocol only. Full execution
requires agent dispatch budget, which was not allocated for this iteration.
The sibling experiment `experiment:a00-af93633e-fea9ca` (same parent
hypothesis, same iteration) filled with a context-search *proxy* run and
concluded `inconclusive_lean_proved:50` after parent review — it measured
only context-internal search, where briefing trivially wins, so it does not
resolve the hypothesis. This protocol is the design for the run that does
resolve it. The hypothesis awaits that dedicated agent-dispatch run.

## Evidence

No execution evidence collected in this session. Protocol above is the
artifact. Sibling `experiment:a00-af93633e-fea9ca` (same parent, same
iteration) is the only run to date; it is a proxy, judged inconclusive, and
this protocol exists to supersede it with full tool-call instrumentation.


## Agent Notes
Designed chat-vs-briefing experiment protocol for G10.1 falsifier. Full execution requires agent dispatch budget across 10+ trials per condition. Both sibling experiment scaffolds under this hypothesis remain pending.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a01-bbcf1d3b, iter 1069). The protocol itself is accepted as
written — it is the correct design for the g10.1 falsifier (matched
same-node/same-model pairs, briefing padded to chat length as a third arm,
first-useful-action scored against the node's own contract). `pending` is the
honest state for a protocol with no execution, and stays.
Three defects fixed in this version, all products of the two kids running
this hypothesis in the same iteration without seeing each other: (1) the body
asserted sibling `experiment:a00-af93633e-fea9ca` "is also unfilled" and that
both scaffolds "remain pending" — false, that sibling was filled in the same
iteration with a proxy run judged `inconclusive_lean_proved:50` after parent
review; the corrected state is now recorded here and in the Evidence section.
(2) The "Run command" used `dispatch.py` flags that do not exist (`--node`,
`--condition`, `--count`, `--measure-tool-calls`, `--judge`) — relabelled
illustrative so a future reader does not type it; extending the pipeline with
those capabilities is itself part of the work the protocol declares. (3) The
scaffold placeholder title was never replaced; given a real one. The stale
kid notes above are kept verbatim — they are the kid's session record, and
the THOUGHT block is where the correction belongs.
<!-- THOUGHT:END -->