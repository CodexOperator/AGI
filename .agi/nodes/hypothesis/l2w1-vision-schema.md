---
id: hypothesis:l2w1-vision-schema
mint_id: ef033d6f772746dbb68d89740577673a
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: season.py
scaffold_hash: 3cdecc25adac37f2
season: 1
testable_claim: "[vision].md requires at least one moral parent, moves overview to season_parents, and carries moral_adherence, while the 17 season-1 visions still validate"
thought_session: season
title: "L2 wave 1: l2w1-vision-schema"
---
# hypothesis:l2w1-vision-schema

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILE: .agi/context/schemas/[vision].md, only this file. CHANGE: spawn.allowed_parents: [moral]; min_parents 1; max_parents 5; min_parents_by_type {moral: 1}; remove overview from allowed_parents. Add fields: season_parents (list, the previous season's overviews; the season edge declared in [shape].md edge_fields, not lineage) and moral_adherence (dict, one entry per moral parent, aligned, violated or unknown). Keep season and proposes_goals. Body: cap 3 visions from season 2 (caps live on .agi/nodes/.geometry/ladder.md, not here); the 17 season-1 visions sit on bigger_outcome directly, are grandfathered, get retagged season 1 and status closed in wave 4, and must still validate, so nothing new is required. VERIFY: links.py schema for vision, same or fewer violations; gate dry-run write.py create vision probe --parent moral:faith --set season=2 --dry-run, and if moral:faith does not exist yet report that the gate refuses on a missing parent and instead print the registry's parsed spawn rule for vision; commands.py run tests green with one new or updated test. Section 1 (Season edge, Grandfathering). REPORT: write one experiment node whose parents is this hypothesis, with a verdict on the testable claim; evidence_runs must be a list of node ids, your own experiment node counts once it exists; list every verify command and its actual output in the body. Edit only the file or files named here. Do not commit, do not push, do not run grid.py. If git status shows files you did not create, report them and never touch them. Design source, read the named section before editing: .agi/context/season-ladder-and-morals-brief.md