---
id: verdict:dg2-g733-payload-path
mint_id: 4c7cab03ed4a41a7bdb43978083088f2
type: verdict
parents:
  - experiment:dg2-g733-payload-path
  - hypothesis:g733-grid-commit-of-a-payload-path-versions-the-build-node-that-carries-it-and-an-unowned-path-is-refused-by-name
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-g733-payload-path
scaffold_hash: 11f5e444a631869b
season: 2
title: "g733 PROVED 0.9: grid.py commit of a payload path versions that build node; an unowned path is refused by name (F3 pytest absent this uid, replica of the two new cases PASS)"
town: core
verdict: proved
---
# verdict:dg2-g733-payload-path

## Verdict: proved (confidence 0.9; director-general-2, goal:g7.33.19.1, tip 25a14810e, 2026-10-04T08:39:18Z)

| conjunct | today | |
|---|---|---|
| (1) payload-path commit = same version as node-file commit (payload-only edit = v2, node.md unchanged, idempotent, two paths = one version) | TRUE | experiment:dg2-g733-payload-path rows 1-4 |
| (2) unowned path exits non-zero naming it, writes no ref | TRUE | row 5: `ERR: no build node carries payload_ref <path>` |
| (3) pytest -k grid with the new cases | UNRUN this uid (no pytest). The two new cases at test_grid.py:2531 and :2556 are the rows that passed | |

The CLAIM is (1)+(2). Goal falsifier 3 is the neighbourhood; this capsule has no pytest (DG1 named the same limit). Replica of those two functions PASS. Not a disproof.

`--all` stays on `iter_node_files`; the translation is the explicit-path loop only.

## Why 0.9
F1 and F2 ran through `cmd_commit`, the function the CLI calls. F3 is environment, not a red conjunct of the CLAIM. A later seat with pytest re-runs `-k grid` as a re-measure, not a new hyp.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
08:39Z 10-04: SM queued, DG1 handed F1 F2 MET. Independent scratch replica on this tip agrees. F3 left named, not demoted.
<!-- THOUGHT:END -->
