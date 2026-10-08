---
id: hypothesis:l2w2-gate-season-parents
mint_id: 6a8adc17ea664d8592d9450bb8149432
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: season.py
scaffold_hash: 1cedac95a4d53cce
season: 1
testable_claim: spawn_gate.py validates season_parents by type from the schema's spawn block, reads current_season from the ladder node, and skips the check for nodes whose season is earlier than the current one
thought_session: season
title: "L2 wave 2: l2w2-gate-season-parents"
---
# hypothesis:l2w2-gate-season-parents

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILE: extensions/agi/bin/spawn_gate.py plus tests in extensions/agi/tests/test_spawn_gate.py; schema files may gain one optional key. RULE: a schema's spawn block may declare season_parents_allowed (list of types); [vision].md gets season_parents_allowed: [overview] (add it, one line). At creation the gate checks every season_parents entry resolves to an existing node whose type is in that list, and refuses otherwise with a one-line reason naming the entry; a type with no season_parents_allowed refuses any season_parents. current_season comes from .agi/nodes/.geometry/ladder.md (field current_season), read once per gate call; a node carrying season lower than current_season, or no season at all while current_season is 1, is grandfathered and skipped. season_parents never count toward min_parents or max_parents (they are the season edge, [shape].md edge_fields role season). VERIFY red-first: vision with season_parents [overview:x] where x exists passes; with a bigger_outcome entry refuses; with a missing node refuses; a season-1 node with anything passes as grandfathered; suite green. Section 1, Season edge and Grandfathering. REPORT: one experiment node under this hypothesis, verdict on the testable claim, evidence_runs as a list of node ids (pass --evidence-runs to cli.py done, your own experiment id counts), every verify command with its actual output in the body. Engine files are edited in place; suite via python3 extensions/agi/bin/commands.py run tests, green before you report; every new rule gets a test that was red first. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them. Design source: .agi/context/season-ladder-and-morals-brief.md