---
id: verdict:dg2close-a00-15d05ac0-7ef787
mint_id: 6bad59482f324d7e9a22068e5f15ec0d
type: verdict
parents:
  - experiment:dg2close-a00-15d05ac0-7ef787-check
  - hypothesis:a00-15d05ac0-7ef787
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2close-a00-15d05ac0-7ef787-check
scaffold_hash: fc5b807ab3d89c60
season: 2
title: "closing (goal:s18 retired): Disproved on the pre-retirement bytes: all 61 kit requirements were verbatim in their build-site hypothesis bodies (and still are in the retired copies); the kit was redundant; moot since L1.09"
town: core
verdict: disproved
---
# verdict:dg2close-a00-15d05ac0-7ef787

| conjunct | observed |
|---|---|
| the requirement text lives ONLY in the kit file, not in the graph | **FALSE**: 61/61 requirements were verbatim in their build-site hypothesis bodies (row 6), and still are in the retired copies (row 9) |
| testable_claim: ≥8/10 sampled cavekit_req carriers lack the AC in their own body | literally TRUE for tasks (10/10, row 5), but 10/10 carry a paraphrased AC subset in their frontmatter (rows 4-5), and each one's parent hypothesis carries the full text (row 8) |
| the node's disproof: ≥6/10 of ITS named sample already contain the AC | **FIRES**: 10/10 (row 7) |
| the inference "the kit is non-redundant, so inlining is mandatory before deprecation" | FALSE: the kit was fully redundant with the graph (row 6) |

**Why disproved.** The hypothesis says the kit held information the graph did not, and the bytes show the reverse. Every kit requirement was already inlined verbatim in a build-site hypothesis node, and the node's own sample fires its own disproof criterion. The narrow per-task literal gap (row 3) is real, but it does not carry the claim, because a task's parent node holds the text. The question is **moot** now: the kits were deleted at L1.09 and the retired hypothesis nodes still hold all 61 requirements (row 9). Confidence is 0.85 rather than higher because the testable_claim's own population (tasks) literally meets its ≥8/10 threshold on body text alone.
