---
id: hypothesis:a00-b5758a12-c77a46
mint_id: 87e3dce7cd0c46c489d2e6bf620c8a54
type: hypothesis
parents:
  - goal:g4.1
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: bd24f8d67ac37274
season: 1
thought_session: season
title: A00 b5758a12 c77a46
verdict: pending
---
# hypothesis:a00-b5758a12-c77a46

## Hypothesis

**Claim:** The duplication pattern recorded in goal:g4.1's THOUGHT block — six of eight kids writing substantially the same hypothesis when aimed at one target — is predictable from the graph's branching structure. A dispatch that fans `spawn.parallel N` across N distinct siblings (child goals or child hypotheses of the target) rather than N copies of the same target drops duplication from >50% to near zero, because the root cause is not the agent harness but the broadcast of one target to N kids who cannot coordinate. The dispatch layer already has the structural information to distribute: every goal node lists its children, and every hypothesis lists its `next_edges`. The missing piece is a dispatch mode that reads this branching topology and allocates each parallel slot to a distinct child.

**Testable shape:** Audit the iteration history recorded in `.agi/config.json` and the loop-runner's log for all instances where `spawn.parallel ≥ 3` was aimed at a single `--target`. For each, classify the N outputs by semantic overlap (proportion sharing the same claim vs proportion covering novel ground). The hypothesis predicts: at N≥3 slots on one target, ≤N/2 outputs are semantically distinct — i.e., ≥50% duplication. At N=8, 6/8 duplication is the known data point (recorded in goal:g4.1's THOUGHT); the audit tests whether this is the rule or the exception.

**Proves it:** ≥3 historical iterations with spawn.parallel ≥3 on one target all show ≥50% duplication. A dispatch change that distributes slots across distinct siblings (partitioned by subtree, one slot per unique descendant) produces >80% distinct outputs in a live trial with N=8 slots.

**Disproves it:** The recorded 6/8 duplication is an outlier — most same-target N≥3 runs show <30% duplication, meaning agents independently choose different open threads even from the same subtree, and the dispatch is already getting adequate coverage from one target. Or: distributed dispatch introduces a new failure — e.g., a slot assigned to a deep subtree produces nothing because the subtree has no actionable open edges, leaving N/2 slots idle.

**Scope:** This hypothesis addresses the dispatch strategy for `spawn.parallel`, not the harness-level collision mechanics, worktree isolation, or command-scoped restriction — those are covered by sibling hypotheses. It also does not propose code changes; it proposes an audit to determine whether a code change is warranted. The fix itself (fan-out dispatch mode reading graph topology) is a separate engineering hypothesis if this one is proved.

**Rationale:** The owner's direction (recorded in the THOUGHT block) states: "spawn.parallel is a THROUGHPUT knob, not a coverage knob. The owner intent was never one target: it is several chains built simultaneously, whole sections of graph at a time." This hypothesis tests whether the dispatch layer's implicit single-target default is the cause of the gap between observed behavior and owner intent. If proved, the fix is structural — change the dispatch default — rather than behavioral (tell kids to coordinate better). The THOUGHT block already names the proposed fix: "several chains built simultaneously, whole sections of graph at a time" — this hypothesis formalizes that design intent as a falsifiable claim.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Written by agent a00-b5758a12 on iteration 1071, extending goal:g4.1. All sibling hypotheses address collision mechanics (worktree, command-scoped isolation, designated committer, stale-.pyc race, agent-prompt fix) — none address the duplication problem the goal's THOUGHT block records as the owner's primary concern. This hypothesis fills that gap by formalizing the dispatch's broadcast-vs-distribution question as a testable claim. The audit method requires only existing logs, not live agent dispatch. The known 6/8 data point from the goal node's own THOUGHT block is the strongest supporting evidence available before the audit runs.
<!-- THOUGHT:END -->


## Agent Notes
Dispatch-duplication hypothesis: same-target spawn.parallel N>=3 produces >=50% duplicate output; proposes fan-out across distinct siblings via graph topology. Fills gap no sibling hypothesis addresses (all existing work addresses collision mechanics, not broadcast duplication).