---
id: hypothesis:l5-a-move-is-proven-by-mint-id-not-basename
mint_id: 31e23c845b78454880d7ba43e883c785
type: hypothesis
parents:
  - goal:g6.18
next_edges: []
confidence: 0.6
edited_by: belam
scaffold_hash: 006bc09953b9ed48
season: 2
testable_claim: A baseline-manifest path absent at HEAD is classified as a MOVE only when the file now present under nodes/deprecated/<type>/<basename> carries the SAME mint_id the baseline path had -- a basename match alone (today's _moved_deprecated logic) is not sufficient, since a deletion paired with an unrelated new file landing at the exact matching deprecated path would be misclassified as a move whenever the compensating arithmetic keeps the total flat. mint_id equality is the proof; a basename match with a different (or absent) mint_id is a LOSS, named, H0/H0b retained.
thought_session: dissolve-legacy-2026-09-19
title: L5 a move is proven by mint id not basename
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-a-move-is-proven-by-mint-id-not-basename

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
