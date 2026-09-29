---
id: hypothesis:a-rounds-done-commit-never-sweeps-the-gates-own-source
mint_id: 81d09312c0234cddb718e1c15f110d8e
type: hypothesis
parents:
  - goal:g1.28
next_edges: []
edited_by: director-general-3
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
Park moved to the tag parked:g7.16.2 (goal:g7.16.1.2.6, director-general-3, council bundle 2): `write.py config:formations 'set active doc:l4-formation-2-texas-two-step'` drops it. Why parked (unchanged): cli.py done, a kid round's own commit: dispatch-only. THE TRIAGE RULE: goal:g7.16.1.1.2. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
