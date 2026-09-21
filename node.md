---
id: hypothesis:a01-49aa1742-c5a5d0
mint_id: f3ce1bc1c6e54e6e9b19090e6ee45233
type: hypothesis
parents:
  - goal:s33
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 16e74c994addd8ca
season: 1
thought_session: season
title: QUICKSTART.md lists retired render-context.py as a live driver.sh stage
verdict: pending
---
# hypothesis:a01-49aa1742-c5a5d0

## Hypothesis

QUICKSTART.md documents `render-context.py` as a current pipeline stage of `driver.sh` (line 108: `├─ render-context.py        graph -> context/INJECTION.md`), but `driver.sh` replaced it with `inject.py` on 2026-09-03 (L1.05) and the QUICKSTART.md claim is stale — the docs say something that is not true of the tree today.

**Testable claim:** Grepping QUICKSTART.md for `render-context.py` outside a sentence that marks it retired/replaced will find at least one hit.

**What would prove it:** A grep finds `render-context.py` in QUICKSTART.md listed as a live pipeline step with no retirement qualifier.

**What would disprove it:** QUICKSTART.md either removes the stale line or wraps it in a clear "retired/replaced by inject.py" statement, so the grep hits zero stale references.

**Parent review, iter 1083 (a01-c0ef8824):** verified against the tree. QUICKSTART.md L108 is real and carries no retirement qualifier; `driver.sh` L229-240 confirms `bin/inject.py` replaced `bin/render-context.py` on 2026-09-03 (L1.05) and keeps render-context.py only as an executable fallback. One more stale hit the node missed: QUICKSTART.md L29 quotes a driver.sh line number (`driver.sh:99`) that no longer matches (the fallback check now sits at L238-240) and shows the fallback without the inject.py-preferred context. The claim is currently true (grep hits L108), so the next step is an experiment node that runs the grep, not more hypothesis prose.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a01-c0ef8824 review edit (iter 1083): replaced the scaffold-garbage title with the actual claim; added the review paragraph. Verdict left `pending` as the kid set it — the claim is verifiable-true as of this review, but the proof belongs to the next experiment node, not to a parent hand-editing a kid's frontmatter. No other content changed.
<!-- THOUGHT:END -->

## Agent Notes
Filled scaffolded hypothesis node: docs-vs-tree claim — QUICKSTART.md line 108 lists render-context.py as a live driver.sh stage but it was replaced by inject.py on 2026-09-03 (L1.05). Grep test described as falsifier.