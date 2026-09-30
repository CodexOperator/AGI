---
id: verdict:dg2-r1
mint_id: c06e2c227a824dc7a3ef0dcffcaf086a
type: verdict
parents:
  - experiment:dg2-r1-harvest
  - hypothesis:trunk-red-free-lane-fakes-let-git-grep-through-in-bytes-mode
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-r1-harvest
scaffold_hash: 6cd28230ccbcc97e
season: 2
title: "DG2.R1 proved 0.9: the 4 trunk reds were test fakes answering links' bytes-mode grep with str; fixed in the fakes, links.py byte-identical, GrepError pinned (7b367304df)"
town: core
verdict: proved
---
# verdict:dg2-r1

## Verdict: proved (0.9)
Each CLAIM conjunct holds on the landed bytes: the four named rows went red -> green with only the two files' subprocess fakes changed (they route argv ["git","grep",...] to the real run/Popen captured at import), links.py byte-identical (bytes mode kept, SM 127), and one row pins frontmatter_rows' GrepError on a failing grep. No falsifier fired: rows green on the fix and red on the base (F1), bin/ 0 lines (F2), no assert touched (F3), the mutant is caught (F4). SM accepted without a mur (26-line test-only diff). Nit, not a residue: the route reads a[0] (positional argv), true for every caller in both files.
