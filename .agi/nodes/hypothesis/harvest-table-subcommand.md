---
id: hypothesis:harvest-table-subcommand
mint_id: 556780f2fec94bc086ee60b58c8c7776
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: master-sensei
scaffold_hash: 24cab1390d35067b
season: 2
testable_claim: "OWNER 2026-09-11 12:4xZ order, master-sensei gen I proposal 3. Grounded in config:rotations `## facts` F5 (sanctuary-director gen XIV calls 12-16,39-40,48,52-54,60,64 -- ~12 calls over 5 rounds discovering, by hand, each round's branch/worktree/diffstat/kid-nodes/verdict). CLAIM: no subcommand in this tree (confirmed by grep: no harvest-table/harvest_table hit anywhere under extensions/agi/bin/) prints, for a live or finished round of a named seat, the five facts F5 lists by hand today: branch (loop/<slug-prefix>-<agent>@s2), worktree path, diffstat against the MERGE-BASE with the seat branch (never a moved seat tip), the round's kid experiment node ids under .agi/nodes/experiment/ on that branch, and each kid's verdict. Add `rotate.py harvest-table --seat <seat> [--round <n>|--all-live]` (or a new harvest.py if rotate.py is already the wrong home -- kid's call, recorded as a deviation if so) that derives all five from the worktree/branch naming convention already in F5, one row per round. FALSIFIER: a live round whose branch/worktree/kid-node-ids/verdict the table gets wrong when checked by hand against the same round. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py or a new extensions/agi/bin/harvest.py (additive subcommand only) + tests."
thought_session: master-sensei-gen1
title: A harvest-table subcommand replaces the ~3-call-per-round hand discovery of branch/worktree/diff/kids/verdict
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:harvest-table-subcommand

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
