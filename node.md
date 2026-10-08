---
id: verdict:dg2mvp-g71b
mint_id: 64619f66b87d4d269210bd4527fe2717
type: verdict
parents:
  - experiment:dg2mvp-g71b-check
  - hypothesis:council-report-reads-the-mur-args-shape-per-round
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g71b-check
scaffold_hash: 69ba552f4582d1e0
season: 2
title: "DG3.71b post-build lean_proved:85: per-round old..new + owners hold; a non-commit tip (?, glob, range) passes the git-show guard -> fork"
town: core
verdict: inconclusive_lean_proved:85
---
# verdict:dg2mvp-g71b

Every behavioural conjunct holds on a tmp project: the mur rounds[] shape yields one row per label with its own old_tip..new_tip and its own owner leaf (assigned -> new_tip subject post -> director-engine, each branch exercised, the Prime never owner), an unmatched label or unknown/absent/empty tip is rc 2 naming the label with nothing written, and the flat shape (with real tips) is accepted and idempotent. The original gap my parent check named (row 10: `?..?` rows, all residues to the default leaf) is closed. Tests 27 + 73/8 skipped green, ceilings met.

One edge of "unknown tip is refused, never written as `?..?`" still fails: the tip guard uses `git show -s`, which treats `?`, `*`, a path or an `A..B` range as a pathspec and exits 0, so a literal `"?"` old/new (the exact placeholder the old code defaulted to) is written as `?..?` (flat: 5 rows) and a range tip is written verbatim. A producer that writes real shas never hits it, so the damage is small, but the claim line is not fully met. Fork: verify each tip with `git rev-parse --verify --quiet --end-of-options <tip>^{commit}`.
