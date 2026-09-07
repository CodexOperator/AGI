---
id: hypothesis:l2w1-report-schemas-floors
mint_id: fc728be1ca7649b78507377dcfe4595e
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: season.py
scaffold_hash: cb7aa67d60d0a7d5
season: 1
testable_claim: "[outcome], [bigger_outcome] and [overview] have min_parents 1 and carry the judgment record and season fields, and every existing node of the three types still validates"
thought_session: season
title: "L2 wave 1: l2w1-report-schemas-floors"
---
# hypothesis:l2w1-report-schemas-floors

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILES: .agi/context/schemas/[outcome].md, [bigger_outcome].md, [overview].md, all three, nothing else. CHANGE per file: spawn.min_parents: 1, drop the min_parents_by_type floors, keep allowed_parents and max_parents. Add optional fields, none required: judged_against (str, the plan node id), lens (str, the plan node's own parent, stamped for readers), alignment (str, regex aligned, adjust or unknown), adjust (str, one line), season (int, already present on overview), season_parents (list, the season edge declared in [shape].md edge_fields, not lineage), and the telemetry roll-ups tokens_in (int), tokens_out (int), cost_usd (float), accepted_bytes (int). [overview] additionally moral_audit (dict with keys faith, love, empathy, antifragility, beauty, each aligned, violated or unknown plus an evidence pointer; document the shape in the body). Body text: replace the floor rationale with the ladder rationale from section 1: a report node is judged against its plan node through the lens above; counts are measured at season close, never enforced as floors. VERIFY: record links.py schema violation counts for the three types before and after, after must be equal or lower; commands.py run tests green; a test asserting the old floors gets updated with a one-line reason. Section 1. REPORT: write one experiment node whose parents is this hypothesis, with a verdict on the testable claim; evidence_runs must be a list of node ids, your own experiment node counts once it exists; list every verify command and its actual output in the body. Edit only the file or files named here. Do not commit, do not push, do not run grid.py. If git status shows files you did not create, report them and never touch them. Design source, read the named section before editing: .agi/context/season-ladder-and-morals-brief.md