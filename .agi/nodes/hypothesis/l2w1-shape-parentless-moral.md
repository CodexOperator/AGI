---
id: hypothesis:l2w1-shape-parentless-moral
mint_id: 060f3da117264fabbc9aca2511d26265
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: director
scaffold_hash: ff5abc5aa6eb8dbe
testable_claim: "[shape].md declares moral as the only parentless type plus three new edge fields, and the spawn gate then refuses a new parentless idea while still accepting a parentless moral"
thought_session: agi-master-2026-09-06
title: "L2 wave 1: l2w1-shape-parentless-moral"
---
# hypothesis:l2w1-shape-parentless-moral

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILE: .agi/context/schemas/[shape].md, only this file. CHANGE 1: parentless_types becomes the single entry moral, with a comment that this is creation-time only: the 113 pre-existing parentless nodes (long-term goals, short-term goals, ideas) are season 1, grandfathered, never re-gated. CHANGE 2: edge_fields gains season_parents {role: season, traversable: false}, grounded_in {role: provenance, traversable: false}, authors {role: provenance, traversable: false}. Leave max_parents_ceiling and ref_namespaces alone. Confirm extensions/agi/bin/spawn_gate.py reads parentless_types from this file (ShapeFacts) and that nothing else hardcodes idea or goal as parentless; a test that asserts the old list gets updated with a one-line reason. VERIFY: python3 extensions/agi/bin/write.py create idea probe --dry-run with no --parent must be REFUSED by the gate; python3 extensions/agi/bin/links.py schema shows no new violations; python3 extensions/agi/bin/commands.py run tests is green; one test for the new parentless list, run red before the edit and green after. If .agi/context/schemas/[moral].md already exists when you run (a parallel kid writes it), also verify write.py create moral probe --set axis=vertical --set grounded_in=Source --set season_introduced=1 --set edited_by=owner --dry-run prints SPAWN-GATE APPROVED; if it does not exist, say so. Section 1 (Grandfathering) and section 3. REPORT: write one experiment node whose parents is this hypothesis, with a verdict on the testable claim; evidence_runs must be a list of node ids, your own experiment node counts once it exists; list every verify command and its actual output in the body. Edit only the file or files named here. Do not commit, do not push, do not run grid.py. If git status shows files you did not create, report them and never touch them. Design source, read the named section before editing: .agi/context/season-ladder-and-morals-brief.md
