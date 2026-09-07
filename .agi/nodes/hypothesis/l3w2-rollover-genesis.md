---
id: hypothesis:l3w2-rollover-genesis
mint_id: 7fb10a09ea1b4fe5858361cb228ae975
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: ubuntu
scaffold_hash: 430bb8253629f363
season: 1
testable_claim: season.py rollover --dry-run on this repo shows the season 1 to 2 plan with the three visions taken verbatim from the brief section 1.8 (text plus gloss, actor owner, parents the five morals, season_parents the season-1 overviews), season 1 named genesis in season_names, and the branch step git checkout -b season/s2, and the real run performs exactly that plan with no invented prose
title: L3w2 rollover genesis
---
# hypothesis:l3w2-rollover-genesis

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
WAVE 2 (brief .agi/context/l3-command-ladder-brief.md sections 1.8, 2.8, 2.9, 3): the kid BUILDS and DRY-RUNS only; the real rollover is run by the prime (Belam) because the visions are minted --actor owner and the season name is the prime's one line. FILES: extensions/agi/bin/season.py (rollover: a --visions-from FILE-or-DIR option taking three markdown files whose bodies are the owner text verbatim; the prime writes those files from the brief section 1.8 before the real run; --name genesis writes season_names on the ladder through write.py; --branch opens season/sN with git checkout -b after the graph writes and prints the next commands, never pushes), .agi/context/schemas/[vision].md and [ladder].md if a field is missing, tests. RULES: never invent or edit vision prose; the dry run must print every node it would mint with its parents, season_parents and actor, and every ladder field it would set, and must refuse while any season-1 overview lacks a judgment (brief 2.9 stage gate) unless --allow-unjudged is given, printing the count. VERIFY: red-first tests on a temp graph for the visions-from path, the name, the refuse-while-unjudged gate and the branch step; on this repo season.py rollover --dry-run --visions-from <dir> --name genesis --branch prints the plan and changes nothing (git status clean afterwards, smoke count unchanged). REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Do not run the real rollover, do not commit, push, or run grid.py commit.
