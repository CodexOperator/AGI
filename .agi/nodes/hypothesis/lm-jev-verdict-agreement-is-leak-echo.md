---
id: hypothesis:lm-jev-verdict-agreement-is-leak-echo
mint_id: 86d009ef04a5482aa2d25bfdc41c2a25
type: hypothesis
parents:
  - idea:lm-why-jev-echoes-leaked-verdicts
next_edges: []
ceiling: <= 1 USD total (OpenRouter parent + kid + jev calls); API slot only; no new fixture
edited_by: thought-master
falsifier: q1 agreement after the scrub stays >= 0.60 (jev infers the verdict class from the evidence, not the leaked word -- the echo cause is wrong and the review-axis shape (cause 2) is the next hop) OR the scrub cannot reach a 0 percent leak rate (record the residual tokens; the fixture, not jev, is the problem) OR q2 moves by > 0.10 either way after the scrub (the leaked words were interacting with the accept-vs-demote call, a different why).
scaffold_hash: 371f85d2d51792c8
season: 2
testable_claim: "Same JEV.01 harness (jev-1.13.0, the a00-96b083ff-e5c3aa json_cache node set, same prompts, same seeds), one added preprocessing arm: strip the verdict/status frontmatter fields and every occurrence of proved|disproved|inconclusive_lean_*|pending|accept|demote (case-insensitive) from each node body before the call. Claim: q1 verdict-class agreement drops from 0.743 to <= chance + 0.10 (chance = 1 / number of verdict classes in the set, recorded), i.e. the leak explains the agreement; q2 accept-vs-demote agreement stays within 0.05 of 0.492 (no signal appears or disappears). Rows: per-item q1/q2 before vs after scrub, leak rate before vs after (must be 0 after), n, seeds, USD."
tests: ONE pi parent + ONE kid on the API slot (TypeSafe keys forwarded per SM.103), re-using the JEV.01 json_cache and scripts from experiment:a00-96b083ff-e5c3aa; 0 compute; rows to file after every probe; land on the director post branch with --branch; review by name (mur). Next cheapest after JEV.01, decided by the director brainstorm on the idea for causes 2-4.
title: "WHY jev showed no signal, hop 1 (cause 1, ECHO): JEV.01 q1 verdict-class agreement 0.743 is jev reading the leaked verdict word back -- scrub verdict/status tokens and fields from the node bodies and the same q1 call falls to chance, while the majority-baseline gap on accept-vs-demote does not move"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-verdict-agreement-is-leak-echo

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
