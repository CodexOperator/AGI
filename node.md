---
id: hypothesis:l3w0-season-retag
mint_id: b70d376584724bfeb7d6e3133a00d23f
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: ubuntu
scaffold_hash: a88a282a056e057e
season: 1
testable_claim: "Every node in .agi/nodes, active and deprecated, carries season: 1 after a scripted write.py pass, so a zoomed-out view can collapse season 1 into one supernode by predicate"
title: L3w0 season retag
---
# hypothesis:l3w0-season-retag

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
MEASURED 2026-09-06: 106 of 1218 active nodes carry season: 1; the rest predate the ladder and were never retagged (node_writer stamps only at mint). CHANGE: a script (extensions/agi/bin/retag_season.py, or a subcommand of season.py, your call, say why) that for every node file under .agi/nodes including deprecated/ with no season field runs write.py NODE set season 1 (never a direct file write; the write guard must stay silent), skipping nodes that already have one and never overwriting; prints counts before and after. Also stamp season on the five moral nodes if absent (they are owner-tier: use --actor owner for those five only, and say so in the experiment). VERIFY: after the run, grep -L on season across .agi/nodes returns nothing; smoke count unchanged (active plus deprecated); write_guard.py check silent; a red-first test on a temp graph with three unstamped nodes. Do not touch node bodies. This is the precondition for the loop and season supernode predicates in brief section 2.7. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Engine files edited in place; suite green via python3 extensions/agi/bin/commands.py run tests; every new rule gets a test that was red first. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them. Design source: .agi/context/l3-command-ladder-brief.md
