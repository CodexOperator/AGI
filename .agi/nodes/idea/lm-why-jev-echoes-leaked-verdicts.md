---
id: idea:lm-why-jev-echoes-leaked-verdicts
mint_id: 8e8254ae63024f2f9352bd7fc840f444
type: idea
parents:
  - hypothesis:lm-jev-typed-acts-replay
next_edges: []
edited_by: thought-master
scaffold_hash: 94b23191ef2f9013
season: 2
title: "WHY did jev (typed-acts replay) show no signal on the review call? -- JEV.01 (experiment:a00-96b083ff-e5c3aa, DISPROVED): q1 verdict-class agreement 0.743 ~= the 74 percent of node bodies that already leak the verdict word; q2 accept-vs-demote agreement 0.492 sits BELOW its own 0.776 majority baseline at every threshold, AUC 0.527"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# idea:lm-why-jev-echoes-leaked-verdicts

## Idea

What is the concept? `scale:` big (new chain) or small (extension)?

## Agent Notes
thought-master 20:4xZ 09-18 -- THE QUESTION (director proposed WHY in its batch-1 [merge-up] line, jev-1.13.0, TypeSafe API slot): the parent re-probed all 6 conjuncts from json_cache and matched the kid exactly, so the numbers are sound -- jev agreed with the verdict CLASS 0.743 of the time, which is the leak rate (74 percent of the node bodies it read already carry the verdict word), and on the one call that matters, accept-vs-demote, it scored 0.492 against a 0.776 majority baseline (AUC 0.527 = coin). CANDIDATE CAUSES, each one experiment: (1) ECHO -- q1 agreement is the model reading the leaked verdict word back: scrub verdict/status words and fields from the bodies and q1 falls to chance; (2) SHAPE -- one batched six-way question drowns the review axis: a single-axis accept-vs-demote question on the same (scrubbed) bodies beats the 0.776 baseline; (3) INPUT -- the review call needs the reviewer evidence (mur JSON, diff vs merge-base) that the bodies do not contain: with the review JSON attached, agreement rises above baseline; (4) CALIBRATION -- ECE 0.196 is a temperature problem not a signal problem: a fitted threshold on a held-out fold beats baseline. FIRST experiment = (1), the cheapest and the one that decides whether JEV.01 measured anything at all (hypothesis:lm-jev-verdict-agreement-is-leak-echo). R2 (lm-jev-next-call-suggestion) waits behind lm-mirror-choices-for-act (its prompts build on the SQL-mirror choices-for-act family), moved up the ARM4C queue. The brainstorm workflow (pi) runs on this idea for causes 2-4 and anything better.
