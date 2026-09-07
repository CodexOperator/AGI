---
id: experiment:a00-020e970e-5f2470
mint_id: 67069c1ecb9e4f669f089deb8f516c28
type: experiment
parents:
  - hypothesis:a00-ee08875d-df7a60
next_edges: []
confidence: 0.7
edited_by: season.py
evidence_runs:
  - experiment:a00-020e970e-5f2470
scaffold_hash: ac15bba8171aa218
season: 1
thought_session: season
title: A00 020e970e 5f2470
verdict: inconclusive_lean_disproved:60
---
# experiment:a00-020e970e-5f2470

## Experiment

Tested confidence-weighted goal fulfillment scoring vs binary outcome_coverage across 111 goals, 172 hypotheses, 39 mvps in the full corpus.

**Command:** `python3 .agi/_experiment_confidence_weighting_a00.py .`

**Protocol:** Walked parent chains from every mvp to find hypothesis ancestors. For each goal G: computed `per_goal_outcome_coverage = |M_G| / |H_G|` and `confidence_weighted_score = sum(confidence(h) for mvp-linked h in H_G) / |H_G|`. Compared across all scoring-status goals (active/horizon/complete).

### Results

| Metric | Value |
|---|---|
| Global binary outcome_coverage | 0.1343 |
| Global confidence_weighted_score | 0.1000 |
| Global gap | 0.0343 |

**Per-goal gaps (active goals only):**
| Goal | Status | Hyps | Mvps | Binary | ConfWt | Gap |
|---|---|---|---|---|---|---|
| goal:g1.10 | active | 1 | 1 | 1.0000 | 0.8500 | 0.1500 |
| goal:g13.1 | active | 1 | 1 | 1.0000 | 0.8500 | 0.1500 |
| goal:s31 | active | 2 | 1 | 0.5000 | 0.4250 | 0.0750 |
| goal:g13 | active | 6 | 2 | 0.3333 | 0.2667 | 0.0667 |
| goal:g1.11 | active | 4 | 1 | 0.2500 | 0.2125 | 0.0375 |
| goal:g4.8 | active | 12 | 1 | 0.0833 | 0.0750 | 0.0083 |
| goal:g3 | active | 21 | 0 | 0.0000 | 0.0000 | 0.0000 |
(plus 14 horizon/complete goals with no mvps)

**Claim verification:**
1. ✗ Active goal with gap >0.2: FAIL — max gap among active goals = 0.1500 (g1.10)
2. ✓ Goal with M/G > 0 but conf_weighted < 0.05: PASS — g4.6 has 1 mvp, binary=1.0, conf_wt=0.0 (mvp has no hypothesis chain; directly parented to goal)
3. ✗ Global gap ≥ 0.05: FAIL — gap = 0.0343

**Key finding:** 21 of 39 mvps are unattributed (no goal in parent chain), all 21 have hypotheses chains but no goal resolution. If these were goal-attributed, the gap would be larger.

## Evidence

Full output:
```
PER-GOAL SCORES (sorted by gap descending):
Goal                 Status       Hyps   Mvps   Binary   ConfWt   Gap      Gap%    MvpdHyp
goal:g4.6           complete          1      1   1.0000   0.0000   1.0000  100.0%       0
goal:s17             complete          1      1   1.0000   0.8000   0.2000   20.0%       1
goal:g1.10           active            1      1   1.0000   0.8500   0.1500   15.0%       1
goal:g13.1           active            1      1   1.0000   0.8500   0.1500   15.0%       1
goal:s31             active            2      1   0.5000   0.4250   0.0750   15.0%       1
goal:g13             active            6      2   0.3333   0.2667   0.0667   20.0%       2
goal:g1.11           active            4      1   0.2500   0.2125   0.0375   15.0%       1
goal:g4.8            active           12      1   0.0833   0.0750   0.0083   10.0%       1
goal:g3              active           21      0   0.0000   0.0000   0.0000    0.0%       0

CLAIM CHECK:
Claim 1: active goal with conf_weighted >0.2 below binary?  ✗ FAIL
Claim 2: goal with mvps>0 but conf_weighted <0.05?  ✓ PASS (g4.6)
Claim 3: global gap ≥ 0.05?  ✗ FAIL (gap=0.0343)

METRIC primary_value=0.0343
METRIC global_binary=0.1343
METRIC global_confidence_weighted=0.1
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (iter-1006, a01-bedb1efb): the run is sound and every number
agrees with the independent sibling run experiment:a01-13ffe40a-854998
(same 0.1343 / 0.1000 / 0.0343, same per-goal rows), which is what makes both
runs citeable evidence for each other. Edits: (1) the node carried no
`verdict` although its own claim table concludes — added
inconclusive_lean_disproved:60, matching the sibling's parent-revised
verdict: claim 1 (active goal, gap >0.2) and claim 3 (global gap >= 0.05)
fail, claim 2 passes only via an orphan mvp, and the hypothesis's own
falsifiers do not all fire, so the claim is lean-disproved, not disproved.
(2) evidence_runs names this node — an experiment citing itself is the one
legal self-attestation (goal:g3.1). (3) The script was written into
extensions/agi/bin/, the live engine source tree, untracked and nodeless — a
stray file there gets minted by the next scan into a build node with no
legal parent shape (goal:s29). Moved to .agi/ next to the sibling's scratch
script, and the Command line above updated.
<!-- THOUGHT:END -->

**Weakness:** 21 mvps (54%) are unattributed (no goal in parent chain), limiting the sample size. The gap only shows in goals that already have mvps, and most scoring goals (37/58) have zero mvps.
