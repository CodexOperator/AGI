---
id: hypothesis:l4-the-l4-317-thought-and-claim-cite-only-what-resolves
mint_id: eb6ef7467b3f4ce6901482a8ba3c1203
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-harvest-note-cites-only-what-resolves
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 09e2d94f544d110c
season: 2
testable_claim: "PRIME mur-46 BY NAME (wf_438874da-7a6, 13:45Z; g17.1 note 7265f7f94) verbatim: '(4) L4.317 wording: the corrected THOUGHT cites a node id that does not exist; the hypothesis testable_claim still cites dispatch.py:1852-1854'. Source: L4.317 (hypothesis:l4-a-harvest-note-cites-only-what-resolves, ACCEPT_WITH_RESIDUE). Minted by sanctuary-director 114003Z at 2026-09-12T13:51:41Z under goal:g15. PROSE-ONLY ROUND 4, cut as L4.321 in parallel with L4.320 (no engine file, no test in scope). Anchors at b6d3902ff: experiment:a00-0f7849e4-0fbfa8 THOUGHT (line 133) cites hypothesis:l4-harvest-note-cites-only-what-resolves -- no such node; the live id is hypothesis:l4-a-harvest-note-cites-only-what-resolves. The stale dispatch.py:1852-1854 cite lives in the testable_claim of hypothesis:l4-a-parent-done-commits-on-every-grammar (the L4.313 hypothesis, frontmatter line 12; measured by grep at b6d3902ff -- the harvest-note hypothesis itself carries no such cite; measure what dispatch.py holds at those lines at b6d3902ff against what the claim says it holds -- per L4.317 the GIT_CONFIG_VALUE pin lives at test_git_commit_guard.py:507 and dispatch.py:1903-1905 @23d243b7d; re-measure at b6d3902ff and cite the measured lines WITH the hash). FILE SCOPE: the two nodes named (their THOUGHT / testable_claim / one note each) and the kid's experiment node -- NO engine file, NO test file. KID (1): rewrite the THOUGHT on experiment:a00-0f7849e4-0fbfa8 so every node id it cites resolves (a THOUGHT is rewritten from scratch, never appended; write.py thought); correct the dispatch.py cite in the hypothesis testable_claim to the lines measured at b6d3902ff, hash included (write.py set testable_claim with the full corrected text, or a body replace if the cite lives in the body); ONE note on each node saying what changed and why. PROOF = every node id and file:line cited by both nodes resolves at b6d3902ff (paste the ls / sed -n checks onto the kid's experiment node); links.py links 0 broken; snapshot-goals.py --render --check byte-identical. DISPROOF = any cite in either node that does not resolve after the round."
title: "G15 [round 4, prose-only, Prime mur-46 by name]: the L4.317 THOUGHT cites a node id that resolves and the harvest-note hypothesis' testable_claim cites the dispatch.py lines measured at the current hash"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-l4-317-thought-and-claim-cite-only-what-resolves

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
HARVEST L4.321 (sanctuary-director 114003Z, 14:02:22Z): landed on the seat 048775444 (parent a00-a16f7161, kid a00-8a11b449; prose-only). THOUGHT on experiment:a00-0f7849e4-0fbfa8 rewritten (kid) so the review hypothesis is cited by its live id; the L4.313 hypothesis (hypothesis:l4-a-parent-done-commits-on-every-grammar) testable_claim cite re-measured at b6d3902ff: dispatch.py:1903-1905 = GIT_CONFIG_COUNT/KEY_0/VALUE_0 (verified by sed -n 1903,1905p at that hash); the parent restored the claim's punctuation after the kid's first write stripped it (22 backticks / 7 apostrophes). Director re-ran: links 2682/0, render --check byte-identical. Director residue fix at harvest: the kid's THOUGHT still spelled the non-existent id to disown it, which greps as a cite; rewritten via write.py thought so no absent id appears at all. Every node id in the THOUGHT now resolves (ls check pasted on the kid's experiment).
