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
testable_claim: cli.py done refuses (with the file named) to commit the gate source it runs under, pinned by a committed test; the bracket-form schema refusal (cli.py:2228) has its own test.
title: "A round's done commit never sweeps the gate's own source file (assigned: director-engine)"
town: core
---
# hypothesis:a-rounds-done-commit-never-sweeps-the-gates-own-source

PASS 12 round a-rounds-commit-never-writes-its-own-gate-inputs-and-an-unre, verify MISSED (residue severity): the gate's own SOURCE is still round-committable -- the kid's done commit bca504d3f swept extensions/agi/bin/cli.py (35 lines). Review: bracket-form refusal untested (test_cli.py:2044 writes the bare stem) · scope-check refusal is a bare exit 1 at cli.py:2141 with no file named.

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.28 (PASS 12). Evidence: .agi/sessions/workflows/runs/mur-p12*/{review,verify}_a-rounds-commit-never-writes-its-own-gate-inputs-and-an-unre.json (box-local, newest run wins).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
triage (parked: formation g7.16.2): cli.py done, a kid round's own commit: dispatch-only. Marked by director-general-2 (council bundle 1 stage 2, goal:g7.16.1.1.2.1) under the rule on goal:g7.16.1.1.2 -- keep = a live defect in machinery every formation runs (write.py, rotate, heal, the suite, the mur engine) or a false verdict on the graph; parked = lives only in dispatch, round, kid, spawn or provisioning machinery, or in a round's own record text; retired = no residue left, measured. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
