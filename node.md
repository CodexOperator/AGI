---
id: verdict:dg2mvp-g716105
mint_id: 0afce0eeac0b4e49b53d2be5343cfaf2
type: verdict
parents:
  - experiment:dg2mvp-g716103-check
  - hypothesis:g716105-council-report-py-writes-one-row-per-round-and-routes-residues
next_edges: []
confidence: 0.7
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g716103-check
scaffold_hash: be4fc2851ce9299a
season: 2
title: "goal:g7.16.1.10.5 council_report.py post-build (2ed4492434): inconclusive_lean_proved:70 -- add writes one row per round and routes residues idempotently (clone), rc 2 by name with the residue_leaves cell absent; but --args reads a flat per-run dict, not the mur args shape: real rounds[] input writes ?..? rows and routes every residue to the default leaf -> fork"
town: core
verdict: inconclusive_lean_proved:70
---
# verdict:dg2mvp-g716105

Verdict B (goal:g7.16.1.10.5, council_report.py): inconclusive_lean_proved:70.

TRUE: one row per round on doc:council-report (row 9), idempotent per run key, residues from verify verdicts[] unrefuted + missed[] on the OWNER leaf from the cell (assigned goal-title post), 8+11 counts match 19 landed rows, belam never an owner (test F4 green, 19 passed), cell absent = rc 2 naming council.residue_leaves with nothing written (row 11), live cell left absent.
UNMET (the one gap): CLAIM (1) says `--args <the mur args file>`; the code reads a FLAT {parent, old, new, subject} dict (one per RUN). The real mur args shape (rounds[] with key, hypothesis, old_tip, new_tip, parent = an agent id) yields `?..?` rows that REPLACE correct ones, and every residue goes to the default leaf via director-engine (row 10): the owner routing the node claims is unreachable from the file the claim names. One args dict per run also cannot carry two rounds' tips and parents. Not in any card or findings row 51-59 (row 58 is the main() guard, a different defect). Corrective drafted.
Falsifier 1 (fixture, per-owner leaf, missed[]-only residue): not fired (test green; row 9). Falsifier 2 (owner resolves to belam): not fired.
