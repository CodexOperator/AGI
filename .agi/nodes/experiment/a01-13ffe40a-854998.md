---
id: experiment:a01-13ffe40a-854998
mint_id: 95563fe7f7ed4cb8ba7c3e8500967268
type: experiment
parents:
  - hypothesis:a00-ee08875d-df7a60
next_edges: []
confidence: 0.6
evidence_runs:
  - experiment:a01-13ffe40a-854998
scaffold_hash: d0956cffefa64115
title: A01 13ffe40a 854998
verdict: inconclusive_lean_disproved:60
---
# experiment:a01-13ffe40a-854998

## Experiment

Tested confidence-weighted goal fulfillment scoring per hypothesis:a00-ee08875d-df7a60.

**Command:** `python3 .agi/_experiment_confidence_weight.py`

**Method:** Loaded all 986 graph nodes, traced parent chains from each mvp upward to find nearest hypothesis ancestor, recorded hypothesis `confidence` field (default 0.5 if missing). For each of 109 scoring goals, computed:
- `binary = mvps_in_subtree / hypotheses_in_subtree`
- `confidence_weighted = sum(hyp_confidence for each mvp) / hypotheses_in_subtree`
- `gap = binary - confidence_weighted`

Also computed global aggregates across all scoring goals.

**Results:**

| Metric | Value |
|---|---|
| Global binary outcome_coverage | 0.1343 |
| Global confidence-weighted score | 0.1000 |
| Global gap | 0.0343 |
| Scoring hypotheses with chain-attached mvps | 15 |
| Scoring mvps with hypothesis chain | 15 |
| Scoring mvps without hypothesis chain (orphan) | 10 |
| Max per-goal gap | 1.0000 (goal:g4.6) |
| Max per-goal gap from confidence alone (excl orphans) | 0.2000 (goal:s17) |

**Per-goal breakdown (goals with non-zero gap):**

| Goal | Hyps | Mvps | Binary | Weighted | Gap | Note |
|---|---|---|---|---|---|---|
| goal:g1.10 | 1 | 1 | 1.0000 | 0.8500 | 0.1500 | hyp conf=0.85 |
| goal:g1.11 | 4 | 1 | 0.2500 | 0.2125 | 0.0375 | hyp conf=0.85 |
| goal:g13 | 6 | 2 | 0.3333 | 0.2667 | 0.0667 | confs=0.75,0.85 |
| goal:g13.1 | 1 | 1 | 1.0000 | 0.8500 | 0.1500 | hyp conf=0.85 |
| goal:g4.6 | 1 | 1 | 1.0000 | 0.0000 | 1.0000 | orphan mvp (no hyp chain) |
| goal:g4.8 | 12 | 1 | 0.0833 | 0.0750 | 0.0083 | hyp conf=0.90 |
| goal:s17 | 1 | 1 | 1.0000 | 0.8000 | 0.2000 | hyp conf=0.80 |
| goal:s31 | 2 | 1 | 0.5000 | 0.4250 | 0.0750 | hyp conf=0.85 |

**Hypothesis confidence distribution (scoring hypotheses only, n=67):**
- 37 with confidence=0.0 (pending — no mvp reached)  
- 4 with confidence=middle (0.3-0.7)
- 16 with confidence=high (0.7-1.0)
- 4 missing confidence (defaulted to 0.5)

## Evidence

**Hypothesis verification:**

| Claim | Expected | Actual | Verdict |
|---|---|---|---|
| 1: At least one **active** goal with gap > 0.2 | True | False (max active gap 0.15, g1.10/g13.1; the >0.2 gaps sit in `complete` goal s17 at 0.20 and complete/orphan g4.6 at 1.0) | ✗ FAIL |
| 2: At least one goal with M/G > 0 but weighted < 0.05 | True | True (g4.6 binary=1.0, weighted=0.0 — but via an orphan mvp with no hypothesis chain, an attribution effect, not low confidence) | ✓ PASS |
| 3: Global gap >= 0.05 | True | False (global gap=0.0343) | ✗ FAIL |

**Final verdict (parent-revised): inconclusive_lean_disproved:60** — written as
disproved because all three proof conditions were expected; claim 3 fails
(0.0343 < 0.05) and, read against the claim's own **active-goal** qualifier,
claim 1 fails too (the >0.2 gaps are in `complete` goals and in an orphan
mvp, not active ones). But the falsification conditions in the hypothesis are
not met either: the weighting has a real, measurable effect (0.0343 global;
0.15 on two active goals), and no falsifier fired. Not proven, not refuted —
lean disproved because the claimed magnitude and the systemic scope both
missed.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (iter-1006, a01-bedb1efb): the run itself is sound — numbers
reproduce exactly against the independent sibling run a00-020e970e-5f2470
(0.1343 / 0.1000 / 0.0343, same per-goal rows). Three edits. (1) Claim 1 was
scored PASS using s17 (gap 0.20, status `complete`) and g4.6 (orphan mvp,
`complete`); the hypothesis's claim 1 says *active* goal, and the max active
gap is 0.15 — so claim 1 FAILS as written. (2) `disproved` without
evidence_runs is a decisive claim that certifies nothing; an experiment may
cite itself, so evidence_runs now names this node, and the verdict is
demoted to inconclusive_lean_disproved:60 — the claim's magnitude and scope
both missed, but the hypothesis's own falsifiers also did not fire, which is
not the same as disproved. (3) Reproducibility hazard the kid did not report:
the cited command `.agi/_experiment_confidence_weight.py` no longer exists on
disk — the numbers are cross-checked by the sibling run, but this node alone
is not reproducible from its own text.
<!-- THOUGHT:END -->

**Key findings:**
1. The systemic gap is small (0.0343). Confidence-weighting has minimal global impact because hypotheses that reach mvps tend to have high confidences (0.75-0.90), and the many pending hypotheses (confidence=0.0) already contribute nothing to either metric.
2. The largest per-goal gap (1.0 for g4.6) is driven by **orphan mvps** with no hypothesis chain, not by low-confidence hypotheses. This is an attribution problem, not a confidence-weighting problem — covered by sibling hypotheses under goal:g3.
3. The largest gap from **pure confidence-weighting** (excluding orphans) is 0.2 for goal:s17 (confidence=0.80 vs binary 1.0), which just meets the threshold but is a single-goal edge case.
4. 10 of 39 scoring mvps are orphaned (no hypothesis chain), contributing 0 weight by the hypothesis's definition. If these are considered true orphans (attribution gap), the confidence-weighting of properly-attached mvps is even tighter.

```json
{
  "global_binary_outcome_coverage": 0.1343,
  "global_confidence_weighted_score": 0.1000,
  "global_gap": 0.0343,
  "claim1_max_gap_gt_0_2": false,
  "claim1_max_gap_gt_0_2_active_only": false,
  "claim2_score_gt0_weighted_lt_0_05": true,
  "claim3_global_gap_ge_0.05": false,
  "max_gap": 1.0,
  "max_gap_goal": "goal:g4.6",
  "verdict": "inconclusive_lean_disproved:60"
}
```

## Agent Notes
Ran full graph traversal on 986 nodes. 109 scoring goals analyzed. Claims 1 (max gap>0.2) and 2 (score>0 but weighted<0.05) pass; Claim 3 (global gap>=0.05) fails at 0.0343. Key finding: the global gap is small (0.0343) because mvps that link to hypotheses have high confidences (0.75-0.90). Largest per-goal gaps come from orphan mvps (no hypothesis chain), not confidence-weighting — an attribution problem handled by sibling hypotheses under g3. Pure confidence-weighting max gap is 0.2 (s17) but not systemic.
