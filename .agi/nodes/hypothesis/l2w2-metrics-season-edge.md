---
id: hypothesis:l2w2-metrics-season-edge
mint_id: f13a1b2d70df43caa9afb05635fb9e0a
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: season.py
scaffold_hash: 17ef9242b03e5e90
season: 1
testable_claim: metrics.py excludes season_parents from chain depth and outcome_coverage by reading the traversable flags in [shape].md edge_fields instead of hardcoding which fields are lineage
thought_session: season
title: "L2 wave 2: l2w2-metrics-season-edge"
---
# hypothesis:l2w2-metrics-season-edge

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILE: extensions/agi/bin/metrics.py plus tests in extensions/agi/tests/test_metrics.py. RULE: the graph walk metrics use follows every edge field whose [shape].md edge_fields entry has traversable: true (today parents and next_edges) and none whose entry is false or absent (season_parents, grounded_in, authors, depends_on, seeds, proposes_goals); the list is read from the schema at run time with the current hardcoded pair as the fallback when [shape].md is missing. VERIFY red-first: a vision with parents [moral:x] and season_parents [overview:y] has chain depth counted through parents only, and outcome_coverage is unchanged by adding a season_parents entry; the metric output on this repo before and after the change is byte-identical (record both); suite green. Section 1, Season edge. REPORT: one experiment node under this hypothesis, verdict on the testable claim, evidence_runs as a list of node ids (pass --evidence-runs to cli.py done, your own experiment id counts), every verify command with its actual output in the body. Engine files are edited in place; suite via python3 extensions/agi/bin/commands.py run tests, green before you report; every new rule gets a test that was red first. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them. Design source: .agi/context/season-ladder-and-morals-brief.md