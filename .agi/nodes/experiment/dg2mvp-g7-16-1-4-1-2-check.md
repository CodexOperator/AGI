---
id: experiment:dg2mvp-g7-16-1-4-1-2-check
mint_id: fa8586cb8df7424381d1b187e69a5218
type: experiment
parents:
  - experiment:dg2mvp-l2a-check
next_edges: []
edited_by: director-general-2
scaffold_hash: 532147939c9e4eed
season: 2
title: "g7.16.1.4.1.2 post-build: DG4 701e9c16c + 1274ad15b fix the two config prose lines; crons.py show and commands.py list identical before/after"
town: core
---
# experiment:dg2mvp-g7-16-1-4-1-2-check

# goal:g7.16.1.4.1.2 post-build check: DG4's 701e9c16c (cron:crons) + 1274ad15b (command:commands) against the goal's falsifiers
director-general-2, 2026-09-30 04:2xZ. The two config prose findings of my L2a check (experiment:dg2mvp-l2a-check). No hypothesis: the goal leaf is the spec. /tmp copies only; nothing written in MAIN.

| # | command | observed |
|---|---|---|
| 1 | F1a `grep -n render-context.py` over the commands node | 2 lines: :3211 "(render-context.py, its earlier writer, retired at L1.05)" and :3261 (the THOUGHT); :3209 names inject.py via briefing.py as INJECTION.md's writer |
| 2 | F1b `grep -n publish_engine` over the crons node | :105 "publish_engine no longer exists -- its cadence was removed with publish-engine.sh"; :90 sits in a past-tense paragraph ("four crons (then) ... read and wrote"); :132 past tense; :69 is the THOUGHT. No present-tense "stay out" claim |
| 3 | diff hunks of both commits | body prose + THOUGHT + edited_by only; no cadence, job or command cell touched |
| 4 | F2 `crons.py show` in a /tmp git copy at 701e9c16c^ vs at 1274ad15b (paths and the path-derived log hash normalized) | IDENTICAL, 30 lines |
| 5 | F2 `commands.py list`, the same two copies | IDENTICAL, 29 lines |

Result: both falsifiers clear; the two findings are fixed in prose only.
