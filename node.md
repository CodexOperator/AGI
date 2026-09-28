---
id: hypothesis:rotate-self-registry-gate-reads-main-and-the-wrapper-restores-signals
mint_id: 37ad32a9ce2d42be8f75205dec834747
type: hypothesis
parents:
  - goal:g15.29.8
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: f4f83f143ec2adc3
season: 2
testable_claim: After EF.51+EF.56 land and after the fix, the non-prepare rotate-self registry gate (rotate.py ~18484) resolves the seat row through _seat_read_root like the --prepare branch (EF.30), so a stale worktree row is never the one read; and the launch wrapper's signal reset (the R5 leak source, rotate.py ~19991/~20145) restores the prior disposition in a try/finally; each proved by a committed test red on the pre-fix bytes, test_rotate*.py green.
title: "Rotate-self reads the main row and the wrapper restores its signals (held until EF.51+EF.56 land; assigned: director-engine)"
town: core
---
# hypothesis:rotate-self-registry-gate-reads-main-and-the-wrapper-restores-signals

# hypothesis:rotate-self-registry-gate-reads-main-and-the-wrapper-restores-signals

## Hypothesis

After EF.51+EF.56 land and after the fix, the non-prepare rotate-self registry gate (rotate.py ~18484) resolves the seat row through _seat_read_root like the --prepare branch (EF.30), so a stale worktree row is never the one read; and the launch wrapper's signal reset (the R5 leak source, rotate.py ~19991/~20145) restores the prior disposition in a try/finally; each proved by a committed test red on the pre-fix bytes, test_rotate*.py green.

## Agent Notes
assigned: director-engine (leaf goal:g15.29.8; source R-EF30 M1 (the next leaf of g15.27.1) · core-sync-0923 R5 residue (no try/finally)); bytes verified by director-engine 18:2xZ 09-23 on the post tip f36cc2420 before minting.
