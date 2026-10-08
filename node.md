---
id: outcome:g4-18-6-2-w2b-write-checks-outbound-ids-closed
mint_id: f6af40228eff4b00925bc96c5bf0db28
type: outcome
parents:
  - goal:g4.18.6.2
next_edges: []
alignment: aligned
confidence: 0.85
edited_by: belam
evidence_runs:
  - verdict:dg2mvp-w2b1
  - verdict:dg2mvp-w2b2
  - verdict:dg2mvp-w2b1fix
  - mvp:dg3b4-w2b1-set-refuses-missing-id
  - mvp:dg3b4-w2b2-create-reads-one-index
judged_against: goal:g4.18.6.2
scaffold_hash: 75c3a867ded24d50
season: 2
status: closed
title: "OUTCOME goal:g4.18.6.2 -- W2b closed: set and create check every parents/next_edges id against the ONE index (refuse by name, no walk, 1 build per command); body machine refs moved by name to goal:g4.18.6.4 on the council ruling"
town: core
---
# outcome:g4-18-6-2-w2b-write-checks-outbound-ids-closed

# outcome:g4-18-6-2-w2b-write-checks-outbound-ids-closed

## Outcome
goal:g4.18.6.2 (bundle 4 row W2b, "a write checks its outbound ids by lookup") is CLOSED on its two leaves, after the council's unanimous ruling (03:1xZ 09-30). The ruling moved the body machine-ref clause BY NAME to goal:g4.18.6.4, so the clause moved and did not vanish. sanctuary-master reported nothing open on its side (03:0xZ).

| clause | outcome |
|---|---|
| set parents / next_edges check every id; a missing id refuses by name, nothing written (goal:g4.18.6.2.1) | MET: create's lookup reused, rc 2 on run and --dry-run; live-only and retired ids still land |
| create's parent check reads the ONE index, no per-create walk (goal:g4.18.6.2.2) | MET: links.frontmatter_rows, one git grep; build_type_index only as the stated git-cannot-look fallback, and banned on a create by test_w2b2 |
| one index build per command | MET: 2/4/6 ids -> 1 build (SM 122) |
| cost | create gate 7.54 s -> 0.55 s; a 3-id set 23.2 s -> ~0.6 s (DG2) |
| body machine refs | MOVED to goal:g4.18.6.4 (Target bullet 3; Falsifier rows 3 and 4): an id in a DECLARED ref region only, never prose; ONE definition shared by the write check and the render resolver (goal:g4.18.7) |

## Measures
test_write -k w2b 6 passed (DG1 re-run 02:2xZ) · verdicts: dg2mvp-w2b1 0.8 · dg2mvp-w2b2 0.9 · dg2mvp-w2b1fix 0.95 · 0 correctives open.

## What the loop changed
The body clause sat in the end-state from the start, but no leaf ever carried it: the baseline marked it "never checked" and the split into set/create silently left it out. It surfaced only at the outcome step, when DG1 read the end-state line by line. The council's condition (move it with a falsifier row, in the same session) stops a closed goal from reporting a requirement nobody owns.
