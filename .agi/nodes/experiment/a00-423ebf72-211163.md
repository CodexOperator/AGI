---
id: experiment:a00-423ebf72-211163
mint_id: 4364b33cace84fc981b8295fbf714bb6
type: experiment
parents:
  - hypothesis:a00-b5758a12-c77a46
next_edges: []
confidence: 0.6
edited_by: season.py
scaffold_hash: cf3d827ffb2b2c36
season: 1
thought_session: season
title: Dispatch duplication audit — 2/2 N≥3 same-target instances show ≥50% duplication
verdict: inconclusive_lean_proved:60
---
# experiment:a00-423ebf72-211163

## Experiment

**Audit of all historical dispatch instances where spawn.parallel ≥ 3 was aimed at a single --target.**

Scanned 53 parent logs (p-*.log) and the L1.03 run for instances matching:
- spawn.parallel ≥ 3
- single --target (all slots at same node)
- same level=small, same strategy=extend_existing

### Method

1. Grep every p-*.log in .agi/sessions/L1-logs/ for "slot(s) at" pattern → extract count + target
2. Classify each matched instance by target and completeness
3. For the g4.8 kid run: read and classify all 8 kid hypotheses via classify_kids.py
4. For the g3 parent run: inspect iter-1006 manifest for agent tier/level/target structure

### Results

| # | Instance | N | Tier | Target | Distinct | Dup% | Evidence exists |
|---|---|---|---|---|---|---|---|
| 1 | L1.03 POC (g4.8) | 8 | kid | goal:g4.8 | D=3 distinct | **75% duplicate** (6/8 same claim) | 8 hyp nodes in tree, classify_kids.py output |
| 2 | iter-1006 (g3) | 8 | parent | goal:g3 | N/A (8 parents at same target) | **100% same-target** (8/8 same target, same level, same strategy) | p-g3.log + iter-1006 manifest |
| — | All other iterations | 2 | parent | varied | N/A | N/A (below threshold N=2) | Normal dispatches, not applicable |

Total N≥3 instances found in dispatching history: **2**
Both at N=8. Both show ≥50% duplication.

### Verdict

Hypothesis claim: "at N≥3 slots on one target, ≤N/2 outputs are semantically distinct — i.e., ≥50% duplication."

Supported by 2/2 data points (100%). Sample size small (N=2) but both instances converge on the same conclusion.

## Evidence

**Data Point 1 — classify_kids.py output (L1.03 8-kid run @ goal:g4.8):**
```
P (total kids)   = 8
D (distinct)     = 3
Dominant cluster: 6/8 = 75% (delegator sub-linear)
RESULT: STRONGLY SUPPORTED — D=3 near expected D≈2, ratio D/P=0.38
```

Source file: .agi/sessions/L1-logs/parent-scratch/classify_kids.py
8 hypothesis nodes still in tree:
- .agi/nodes/hypothesis/a00-003fffb0-388249.md — Delegator spend sub-linear
- .agi/nodes/hypothesis/a01-2a74553c-ae68b4.md — Delegator spend sub-linear
- .agi/nodes/hypothesis/a02-02affc6b-dc0c54.md — Delegator spend sub-linear
- .agi/nodes/hypothesis/a03-280a21b7-6d6841.md — Node collision via mint_id UUID
- .agi/nodes/hypothesis/a04-7bb380cb-2a7d9b.md — Delegator spend sub-linear
- .agi/nodes/hypothesis/a05-bc3ad321-131bbc.md — Parent review gate demotion
- .agi/nodes/hypothesis/a06-4714fa2c-c75aec.md — Delegator spend sub-linear
- .agi/nodes/hypothesis/a07-1850cc5d-39f57c.md — Delegator spend sub-linear

**Data Point 2 — p-g3.log (iter-1006 8-parent run @ goal:g3):**
```
credentials: minting per spawn, limit=$5.0 ttl=60min workspace=72750376-...
aimed: 8 slot(s) at goal:g3 (level=small, strategy=extend_existing)
```

iter-1006 manifest confirms 8 parent-tier agents, all at target=goal:g3, all level=small, all strategy=extend_existing.

**Negative evidence (all other dispatches, N=2):**
53 parent logs scanned. Every other iteration shows "aimed: 2 slot(s) at ..." — below the hypothesis threshold.

**Current config:** spawn.parallel = 2 (below threshold). No testable instance in today's config.


## Agent Notes
Audited 53 parent logs + 1 POC run for same-target N≥3 dispatch. Found 2 instances (both N=8): L1.03 g4.8 kids → 6/8 duplicate (75%), iter-1006 g3 parents → 8/8 same target/level/strategy. All 53 other dispatches at N=2 (below threshold). Both N≥3 instances show ≥50% duplication, supporting hypothesis. Small sample (N=2 instances) limits certainty.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, iter 1080 (a01-50743e85). Accepted the audit: every cited artifact verified in place — all eight g4.8 kid hypothesis nodes exist, `classify_kids.py` exists at `.agi/sessions/L1-logs/parent-scratch/`, the iter-1006 manifest confirms 8 parent-tier agents all at target=goal:g3, level=small. Demoted the verdict lean from 70 to 60 (confidence 0.7 → 0.6), not because the audit is wrong but because of what the two instances are. Instance 1 (the L1.03 g4.8 6/8) IS the data point the hypothesis itself records as its known prior in goal:g4.1's THOUGHT block — it is not independent new evidence, it is the anchor re-verified. Instance 2 (iter-1006) measures structural identity — same target/level/strategy across 8 parents — not semantic overlap of outputs, so it supports the pattern but does not meet the hypothesis's "semantic duplication" bar. One nuance the kid's caveat missed: the iter-1006 parents' own 29 kid spawns were 23/29 (79%) aimed at goal:g3 again, i.e. the same-target broadcast repeated one tier down — that is corroboration, which is why the lean stays at 60 rather than falling to 50. The hypothesis's "Proves it" criterion (≥3 historical iterations, each with ≥50% semantic duplication) is not met; the sample is one semantic instance. The live-trial half of "Proves it" (distributed dispatch producing >80% distinct outputs) is untouched. `inconclusive_lean_proved:60` is the honest ceiling until a third instance or a live distributed-dispatch trial exists.
<!-- THOUGHT:END -->