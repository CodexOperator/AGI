---
id: hypothesis:lm-rotate-status-uses-canonical-season-branch
mint_id: e1674cf5dd9247a5bb3c65607283b184
type: hypothesis
parents:
  - goal:g7.33.3
next_edges: []
confidence: 0.95
edited_by: belam
scaffold_hash: 138859d6fb206277
season: 2
tags:
  - engine
  - local-maxxing
testable_claim: "Today rotate.season_branch starts from the legacy ladder spelling season/s{N} and passes it to branches.ref_candidates, which parse()s the alias and prints branches.py: deprecated alias used: season/sN -> seasonN/main on every rotate.py status --record call (reproduced on belam). CLAIM: season_branch feeds ref_candidates the CANONICAL season{N}/main first (legacy only as fallback / neither-on-origin / root is None ladder spelling), so status --record on a tree where origin/season2/main exists prints NO deprecated-alias warn and still returns season2/main. FALSIFIER: (a) status --record still warns season/s2 -> season2/main on this tree; (b) when only origin/season/sN exists, season_branch invents a canonical that resolves nowhere; (c) season_branch(None) changes from season/s2. TEST: test_g7333_be_where_season.py (canonical-first no warn · legacy-when-only-alias · None ladder). FILE SCOPE: extensions/agi/bin/rotate.py season_branch + the focused test. CEILING: source-suffix lines; data files never count."
title: "G7.33.3(e): rotate.py status uses canonical season{N}/main — no deprecated-alias warn"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-rotate-status-uses-canonical-season-branch

# hypothesis:lm-rotate-status-uses-canonical-season-branch

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Belam NO-PI 2026-09-28: g7.33.3(e) landed — `rotate.season_branch` feeds `branches.ref_candidates(canonical)` (`season{N}/main`) instead of the legacy ladder alias, so `rotate.py status --record` no longer prints `branches.py: deprecated alias used: season/s2 -> season2/main`. Focused tests 5/5 in test_g7333_be_where_season.py; live status smoke: alias warn absent.
