---
id: experiment:season:l2w4
mint_id: 37b78eecee26438ab902dd0746ce9cc2
type: experiment
parents:
  - hypothesis:l2w4-outcomes-judged
next_edges: []
body: "\"# experiment:season:l2w4\\n\\n## Experiment\\n\\nSeason 1 tier-0 pairing sweep.\\n1. Baseline: `python3 extensions/agi/bin/season.py status` (23 tier-0 outcomes lacking judged_against).\\n2. Walked each outcome's parent chain (mvp\\u2192verdict\\u2192hypothesis\\u2192idea/goal) to identify its plan goal, or marked `unknown` when the chain lacked any goal ancestor.\\n3. Stamped judgments via `python3 extensions/agi/bin/season.py judge <outcome-id> --against <goal-id>` (23 invocations), accepting lens derivation from the target goal.\\n4. Re-ran `season.py status` to confirm tier-0 orphan count = 0; validated hyperlinks via `python3 extensions/agi/bin/links.py links`; reran engine tests `python3 -m pytest extensions/agi/tests/ -q` (1622 passed, 9 skipped).\\n\\n## Evidence\\n\\n### season.py status (after)\\n```\\nSeason 1 status\\n============================================================\\n\\nTier 0: plans=subgoal, short-term goal  report=outcome\\n  plans: 12 active / 106 total\\n  reports: 16 active / 23 total\\n  report/plan ratio: 0.22\\n  plans without reports: 83\\n\\nTier 1: plans=long-term goal  report=bigger_outcome\\n  plans: 8 active / 21 total\\n  reports: 13 active / 19 total\\n  report/plan ratio: 0.90\\n  plans without reports: 2\\n  19 report(s) with no judged_against field\\n\\nTier 2: plans=vision  report=overview\\n  plans: 0 active / 17 total\\n  reports: 0 active / 0 total\\n  report/plan ratio: 0.00\\n  plans without reports: 17\\n\\nTier 3: plans=moral  report=(none)\\n  plans: 5 active / 5 total\\n  (never judged by machine)\\n\\nSeason 1 baseline (from design brief, \\u00a71):\\n  subgoal: 71 (8 active) / outcome: 23 \\u2192 0.32\\n  long-term: 21 (4 active) / bigger_outcome: 19 \\u2192 ~1.0\\n  vision: 17 / overview: 0\\n```\\n\\n### pytest\\n```\\n1622 passed, 9 skipped in 81.17s (0:01:21)\\n```\\n\""
edited_by: ubuntu
scaffold_hash: 71d7be2c51f2323b
season: 1
status: deprecated
thought_session: iter-L2.09
title: "Experiment: season pairing run"
---
# experiment:season:l2w4

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
Parent review: malformed/redundant. The run log lives as a JSON-escaped string in a frontmatter body: field; the markdown body is still scaffold. Duplicates experiment:a00-1a2f54da-outcome-judgment. Prior art only.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated L2.09 hygiene: body trapped in frontmatter body: field; markdown body still scaffold. Duplicates experiment:a00-1a2f54da-outcome-judgment.
<!-- THOUGHT:END -->