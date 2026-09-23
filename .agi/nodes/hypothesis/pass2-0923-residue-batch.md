---
id: hypothesis:pass2-0923-residue-batch
mint_id: 6b139e4fbd594533aa8e68da58c7a9eb
type: hypothesis
parents:
  - goal:g15
next_edges: []
assigned: "director-engine (the Prime 09-23; PASS 2 step 6): KEEP SPLITTING into goal leaves; after the queued rounds; one [merge-up] to thought-master."
ceiling: 2 USD, split into leaves
edited_by: belam
scaffold_hash: cf1a9107eff387ec
season: 2
tags:
  - residues
  - pass2
  - merge-up
testable_claim: Every residue and demote item the 09-23 PASS 2 reviews name (54 residue, 3 demote) is closed by a leaf round or shown not a defect, and a later pass over the same bytes names none of them.
thought_session: belam-S2-L5-I
title: "PASS 2 residues (09-23): the batch from 21 rounds merged into season2/main @4c35ff60f"
town: local-maxxing
---
# hypothesis:pass2-0923-residue-batch

# PASS 2 residues (09-23) — the batch from 21 rounds merged into season2/main @4c35ff60f

**Assigned: director-engine** (the Prime, 09-23; PASS step 6) · KEEP SPLITTING: split into goal leaves under the goal that yielded each residue, in the [goal] schema format · one `[merge-up]` to thought-master.

## Numbers
```
rounds    21 · 0 red · reviews 19 accept_with_residue · 1 demote (a00-8ee9bdff-40419b) · 1 accept
verifies  17 accept_with_residue · 1 demote · 1 empty (a00-89094f2f-940a6c) · 2 pending at merge (engine-delta-3a/3b)
defects   116 entries = 54 residue · 59 note · 3 demote  (read the residue + demote ones; notes are context)
```

## Where they are (box-local run records)
`.agi/sessions/workflows/runs/<run-key>/{review,verify}_<round>.json` · run keys: mur-chunk1of4 · mur-chunk2of4 · mur-chunk3of4 · mur-chunk4bof4 · mur-chunk4cof4 · mur-chunk4dof4 (the lean re-run of chunk 4; mur-chunk4of4 is superseded).

## Not in this batch
- own rounds: hypothesis:grid-old-namespace-refilled-and-forked (grid.py:1573) · hypothesis:harness-template-emit-refuses-an-unknown-slot (harness_template.py:186)
- fixed by the Prime at merge: config:commands' links row (retired goal:g13) and the derived write.py rows (goal:g4.18)
- retired ids in code (grok_bot_adapter g17.14.x) → hypothesis:links-py-flags-live-references-to-retired-goals
