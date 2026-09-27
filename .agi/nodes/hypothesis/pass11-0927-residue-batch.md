---
id: hypothesis:pass11-0927-residue-batch
mint_id: 4af032c7eb634ec3933c7328c34430ce
type: hypothesis
parents:
  - goal:g1.27
next_edges: []
edited_by: belam
scaffold_hash: b2a2369f824ed2e8
season: 2
status: open
testable_claim: The falsifier grep of goal:g1.27 returns 0 hits and each row below is fixed at its cited line.
title: "PASS 11 doc and skill residue batch: no text names the paid route, points past its block, cites a wrong line, or hand-copies the skill index (assigned: director-engine)"
town: core
---
# hypothesis:pass11-0927-residue-batch

# hypothesis:pass11-0927-residue-batch

PASS 11 residue table (verify-upheld; run mur-p11chunk1of1):
| # | where | residue |
|---|---|---|
| 1 | skills/agi-rotate/SKILL.md:12 | facts pointer `read body 37:64` -- the region is 37:57 since cdcfe5c0b |
| 2 | skills/agi-master-gate/SKILL.md:55 | cites rotate.py:16159 (a bare pass); the mirror gate is rotate.py:4053 branches.mirror_and_prove in _prepare_merge_target |
| 3 | extensions/agi/briefs/director-belam-duties.md:5, master-sensei-duties.md:5, sensei-director-duties.md:3 | 'a review by name on pi' (the PAID harness) + a hand-copied skills index that the startup `skills` entry now loads (owner 05:33Z: no duplication) |
| 4 | extensions/agi/workflows/round-research-review.json:7 | description still 'Requires --harness pi' against its own provider pi-free |
| 5 | .agi/config.json:200,205,210 | workflows notes still name provider pi / the pi harness |
| 6 | .agi/nodes/build/bin-provisioning.md:121 | BUILD-CONTRACT stale: can_fund at line 177 with the old signature |
| 7 | skills/agi-dispatch/SKILL.md:36 | hardcodes '<= 8 live parents' while values.local_maxxing.de_live_parents is the cell |

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.27 (PASS 11).
