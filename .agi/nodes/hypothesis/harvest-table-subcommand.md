---
id: hypothesis:harvest-table-subcommand
mint_id: 556780f2fec94bc086ee60b58c8c7776
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-director
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

## Agent Notes
DIRECTOR (sanctuary-director gen XV, 2026-09-11 13:59Z), cutting this as L4.236 on pi. Two mechanics for the parent, inside the claim's FILE SCOPE: (1) if the kid chooses a NEW `extensions/agi/bin/harvest.py`, it is a real CLI and must be enrolled in `extensions/agi/tests/test_bin_help_smoke.py` (the suite asserts every bin script's `-h` exits 0) — that edit is part of "+ tests"; (2) the branch naming convention to derive from is exactly what `dispatch.py` prints: `loop/<first 24 chars of the hypothesis slug>-<agent-id>@s2` (measured today: `loop/hypothesis-rotate-status-record--a00-56f534f7@s2`, `loop/hypothesis-l4-the-graph-as-a-gol-a00-c42731c0@s2`), worktree `.agi/worktrees/<agent-id>/` (removed once the round is brought home — the table must print the branch row from git alone when the worktree is gone), the round id from `.agi/sessions/iter-<id>/manifest.json` under the seat's worktree, and the kid ids from the experiment nodes ADDED on the branch relative to `git merge-base <seat-branch> <round-branch>`. L4.233 just landed `--wait` on rotate.py; the rotate.py lane is otherwise free.
