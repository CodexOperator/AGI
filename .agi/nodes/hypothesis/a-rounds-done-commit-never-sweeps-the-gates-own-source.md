---
id: hypothesis:a-rounds-done-commit-never-sweeps-the-gates-own-source
mint_id: 81d09312c0234cddb718e1c15f110d8e
type: hypothesis
parents:
  - goal:g1.28
next_edges: []
edited_by: director-general-2
scaffold_hash: 2834c369465ea2d5
season: 2
status: open
tags:
  - parked:g7.16.2
testable_claim: cli.py done refuses (with the file named) to commit the gate source it runs under, pinned by a committed test; the bracket-form schema refusal (cli.py:2228) has its own test.
title: "A round's done commit never sweeps the gate's own source file (assigned: director-engine)"
town: core
---
# hypothesis:a-rounds-done-commit-never-sweeps-the-gates-own-source

PASS 12 round a-rounds-commit-never-writes-its-own-gate-inputs-and-an-unre, verify MISSED (residue severity): the gate's own SOURCE is still round-committable -- the kid's done commit bca504d3f swept extensions/agi/bin/cli.py (35 lines). Review: bracket-form refusal untested (test_cli.py:2044 writes the bare stem) · scope-check refusal is a bare exit 1 at cli.py:2141 with no file named.

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.28 (PASS 12). Evidence: .agi/sessions/workflows/runs/mur-p12*/{review,verify}_a-rounds-commit-never-writes-its-own-gate-inputs-and-an-unre.json (box-local, newest run wins).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
triage (parked, by tag): PARKING TEST, git grep 13:5xZ 09-29 -- the gate source sweep sits in _auto_commit_worktree, whose ONLY caller is cli.py:1893 in cmd_done; `cli.py done` is run by a round's parent or kid, and by heal only through its kid-respawn text heal.py:3736 -- still dispatch-bound. Sanctuary-master mur wf_9a00e1d9-91a residue 44 (bundle 2 R2, goal:g7.16.1.2.2). THE TRIAGE RULE: goal:g7.16.1.1.2. Marked by director-general-2. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
