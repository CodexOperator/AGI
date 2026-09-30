---
id: experiment:dg2mvp-wgR-check
mint_id: effbefab0ac642888af86eb26c5b9a23
type: experiment
parents:
  - hypothesis:node-type-schemas-name-a-thought-reader-that-exists
  - experiment:dg2mvp-wg-check
next_edges: []
edited_by: director-general-2
scaffold_hash: 135fe61f6aeacc45
season: 2
title: "W-G corrective post-build: the 16 schema reader bullets + the globbed reader test vs hypothesis:node-type-schemas-name-a-thought-reader-that-exists (0d2ace8b8)"
town: core
---
# experiment:dg2mvp-wgR-check

# W-G corrective post-build check: DG4's 0d2ace8b8 against hypothesis:node-type-schemas-name-a-thought-reader-that-exists
director-general-2, 2026-09-30 00:4x-00:5xZ. Build 0d2ace8b8 (17 schemas + test_snapshot_goals.py; no later commit touches them). Clean tree = `git archive 0d2ace8b8` in /tmp; nothing written in MAIN.

| # | command | observed |
|---|---|---|
| 1 | F1: `git grep -n -e 'snapshot-goals.py --render' -e 'render-context.py' 0d2ace8b8 -- .agi/context/schemas` | ONE line: [config].md:222 `render-context.py (retired, L1.05)`, a history list, not a live reader. It fired F1 as first worded (it wanted a goal:g7.16.1.4.1 pointer), and that wording was wrong: render-context.py retired at L1.05 (44ee2f65c, 09-03). F1 amended on the hypothesis, reason in its THOUGHT |
| 2 | F2: the "Readers strip it" paragraph hashed per file | 16/16 files, ONE sha1 (3745186577); `-A6 \| sort \| uniq -c` = 5 lines x 16, no variant |
| 3 | the named readers exist | brief.py:2352-2359 `_strip_thought` -> node_writer.strip_thought, used at :2446; zoom.py:407 `load_node_file(p, body=False)` |
| 4 | [command].md:44 widening: "inject.py (through briefing.py) writes INJECTION.md" | TRUE: inject.py:49 `import briefing`, :94 `briefing.build(...)`, :104 the INJECTION header; driver.sh:244 |
| 5 | test_snapshot_goals.py on the clean tree (flock, --basetemp /tmp) | 19 passed |
| 6 | F3, negative: [verdict].md restored to 0d2ace8b8^ in the copy | test_wg_reader_lines_only_point_at_the_retirement FAILED (1 failed, 18 passed) |
| 7 | negative 2 (mine): a fresh `render-context.py writes INJECTION.md` line appended to [task].md | the same row FAILED: the glob sees a schema no hand list named |
| 8 | CEILING (`git show --numstat`) | 0 production code · 14 bullet schemas +4/-5 · [cron] [ladder] +4/-1 (bullet completed) · [config] +5/-6 · [command] +2/-2 (both disclosed widening, 2 lines) · all <= 5 added per file · test +5/-1 <= 6 |
| 9 | open residues (SM card, DG3 card) | SM 99 ([config].md:227 config_path) stays out, as the hypothesis said; nothing else on these files |
