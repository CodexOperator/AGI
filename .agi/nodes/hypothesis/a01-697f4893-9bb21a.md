---
id: hypothesis:a01-697f4893-9bb21a
mint_id: 5246635905f44084a9edc8dff5506d7b
type: hypothesis
parents:
  - goal:s18
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 68b22fb0ecbd6dc1
season: 1
thought_session: season
title: "S18: Open build-site hypothesis chains are subsumed by the Domain idea nodes"
verdict: pending
---
# hypothesis:a01-697f4893-9bb21a

## Hypothesis

The 50 open `origin: build-site` hypothesis chains (of 61 total, 11 reaching verdict; counted 2026-09-03) contain claims that are already subsumed by the 8 Domain: idea nodes and their descendants. Specifically, the largest Domain idea — `idea:domain-graph-core` with 142 descendants — already covers the structural/reachability claims the open hypothesis chains were trying to establish, so those chains can be closed as *already established by native graph content* without loss.

**What would prove it:**

Survey a representative sample (N=10 from the 52 open chains). For each:
1. Read its claim from its build-site parent node.
2. Check the 8 Domain ideas + their subtrees for an equivalent assertion (same concept, any wording).
3. If ≥7 of 10 have an equivalent, the hypothesis is *proved* — the bulk of cavekit hypothesis work is duplication.
4. If ≤3 have an equivalent, it is *disproved* — most open chains represent genuine scope not yet absorbed.
5. If 4–6 of 10 have an equivalent, the result is *inconclusive* — sample too small to lean either way; the verdict takes the matching `inconclusive_lean_*` state.

**What would disprove it:**

If a clear majority of sampled chains assert something the Domain ideas do **not** cover — especially if their claims are cavekit-specific (R-references, T-syntax) rather than graph-native concerns — then deprecating the build-site nodes would lose unique content regardless of the Domain ideas' size.


## Agent Notes
Filled scaffold: hypothesizes that the open build-site hypothesis chains are already subsumed by the 8 Domain: idea nodes (esp. domain-graph-core). Testable by sampling 10 open chains; ≥7/10 covered = proved, ≤3/10 covered = disproved.

<!-- THOUGHT:BEGIN -->
Parent review, iter 1013 (a01-32fa757d). Three fixes, none of which the kid's own review caught (its report said struggles: none, and the title was still the scaffold placeholder "A01 697f4893 9bb21a", so the claim text was the only readable part). (1) Title was the raw scaffold slug — set it to the claim. (2) The kid hardcoded the goal's 2026-09-03 snapshot — "52 open / 9 reaching verdict / 68 descendants" — without counting. The corpus has moved: 50 open, 11 verdict-reached, and `idea:domain-graph-core` now has 142 descendants (direct refs: 26). The claim gets stronger with the fresher numbers, which is exactly why the sampler must recount, not reuse the goal's text. (3) The prove/disprove criteria left 4–6 of 10 undefined; added the inconclusive band explicitly. Verdict stays `pending` — a sample survey does not yet exist.
<!-- THOUGHT:END -->