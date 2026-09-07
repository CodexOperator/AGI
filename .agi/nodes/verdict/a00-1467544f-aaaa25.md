---
id: verdict:a00-1467544f-aaaa25
mint_id: 9f467422284d4fc7a214305898bb29c6
type: verdict
parents:
  - exp:a00-1467544f-aaaa25
next_edges:
  - mvp:a00-1467544f-aaaa25
confidence: 0.97
contradicts: []
edited_by: season.py
evidence_runs:
  - exp:a00-1467544f-aaaa25
season: 1
status: proved
supports: []
tags:
  - bootstrap
  - chain-engine
thought_session: season
title: "Hypothesis task-spawns bootstrapping: PROVED"
verdict: proved
---
**Verdict:** PROVED (confidence: 0.97)

**Claim:** ≥70% of hypothesis nodes spawn ≥1 task via the `spawns` relationship, providing sufficient graph density for chain bootstrapping.

**Evidence:**
- traversability_ratio = 0.9677 (96.77%)
- 60/62 hypotheses have ≥1 task child
- 88 total hypothesis→task edges
- avg 1.42 tasks per hypothesis
- All 7 domains show ≥90% traversability

**Threshold check:** 0.9677 ≥ 0.70 → PROVED

**Implication:** The capillary DAG has high hypothesis→task density. The primary bottleneck for chain formation is NOT graph density but rather:
1. Missing `next_edges` connecting ideas → hypotheses → experiments → verdicts → app_purpose
2. Missing intermediate node types (experiment, verdict, mvp, outcome, bigger_outcome, app_purpose)
3. No `app_purpose` nodes (required for chain completion)

**Next step:** Add `next_edges` from ideas to hypotheses and hypotheses to experiments to enable `find_chains()` traversal.