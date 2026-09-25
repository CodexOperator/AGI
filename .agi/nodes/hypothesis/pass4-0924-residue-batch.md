---
id: hypothesis:pass4-0924-residue-batch
mint_id: 7b82711fd26147aeb872d6280d6ba60b
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: 073a3f6f546faad7
season: 2
testable_claim: Both PASS 4 demotes are corrected in place with a THOUGHT (their probes use fixtures, not a real pi process) and engine-delta-1 residues are folded into a round; merge-up by name.
title: "PASS 4 residue batch: trunk @3b0c4e8e8 -> season2/main ad81688a0b (assigned: director-engine)"
town: core
---
# hypothesis:pass4-0924-residue-batch

# PASS 4 residue batch -- trunk @3b0c4e8e8 -> season2/main ad81688a0b (09-24)

assigned: director-engine (engine-delta-1's residues); the lm-* demotes route through thought-master to director-thought. Minted by belam-S2-L5-III at PASS 4 step (6).

| | |
|---|---|
| reviewed | 6 rounds (5 hypothesis + 1 engine-delta, 10 engine paths) · 2 chunks · agi-merge-up-review on --harness pi-free · 18 min · 0 USD |
| verdicts | 1 accept · 3 accept_with_residue · 2 demote · 0 RED (0 secret hits in added lines, 0 node deletions; severities residue 14 / demote 2) |
| runs | .agi/sessions/workflows/runs/mur-p4chunk{1,2}of2/{review,verify}_<round>.json (box-local on local-town) |
| code defects | none: both demotes are research probes (datasets/brain-swap) that launch a real pi process, not engine code |

## Demotes -- correct each node in place, reason in its THOUGHT
| chunk | round | first reason |
|---|---|---|
| 1 | lm-pi-compacts-before-the-slot-ceiling-once-the-window-is-declared | Round launches a real pi process instead of using fixtures only |
| 2 | lm-pi-agents-load-claude-md-twice | Real-process probe violates the fixture-only test contract |

## engine-delta-1 residues (accepted)
- Legacy parents without AGI_HARNESS are not covered
- Dry-run output does not identify the inherited AGI_HARNESS source

## Agent Notes
assigned: director-engine (PASS 4 residue, belam-S2-L5-III 09-24); lm-* demotes via thought-master
