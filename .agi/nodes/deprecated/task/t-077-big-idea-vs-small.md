---
id: task:t-077
mint_id: 4e0651cda1d04e13a047f1f23684441a
type: task
parents:
  - hyp:autoresearch-tree-skill-r2
acceptance_criteria:
  - R2.1 (each iteration emits record naming chosen path before any agent dispatched)
  - R2.2 (probability of big-idea path equals configured big_idea_vs_small_idea_split)
  - R2.3 (two consecutive iterations with same seed + config → same choice)
  - R2.4 (config value missing or out of range → iteration aborts with structured error)
blocked_by:
  - task:t-053
cavekit_req: autoresearch-tree-skill/R2
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-077: Big-idea-vs-small-idea decision per iteration (with seed determinism)"
---
**Description:** Implement `decide_path(seed, config) -> Literal['big', 'small']`. Use `random.Random(seed)` to draw and compare to `big_idea_vs_small_idea_split`. Persist the decision record at `context/iterations/<n>/decision.json`. Validate config range [0.0, 1.0] before drawing.

**Files:** `agi-tree/src/skill/decision.py`, `agi-tree/tests/skill/test_decision.py`

**Test Strategy:** Tests for each criterion. Statistical test: 1000 draws with split=0.3 → big-count within 95% binomial CI.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `autoresearch-tree-skill/R2` under `hyp:autoresearch-tree-skill-r2`, whose disposition is disposition GENUINELY-OPEN, not run: no seeded big/small binary-decision mechanism was found in `dispatch.py`/`driver.sh` (uncertain rather than confident -- the full iteration-selection logic was not traced); `goal:g4.6`/`goal:g4.7` are this domain's real goals and do not obviously cover this item, so this THOUGHT is the record.
<!-- THOUGHT:END -->
