---
id: hypothesis:lm-jev-split-leaks-repeats
mint_id: 63fcb238f8534e3786001492cfb5e707
type: hypothesis
parents:
  - idea:lm-why-verdict-ece-ignores-temperature
next_edges: []
edited_by: brainstorm
loop: mvp:lm-research-review-workflow@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 7efd2580c28d9509
season: 2
testable_claim: Re-splitting the committed q1 rows (json_cache_scrub + acts_replay_scrub.jsonl, 0 new API calls) with ALL 3 repeats of an act id forced onto the SAME side (GroupKFold by act id) drops verdict-subgroup held-out ECE from 0.141-0.212 to <= 0.10 on >= 4/5 seeds; if it stays > 0.10 the split was not the artifact.
thought_session: iter-TM.60
title: "WHY hop 6a: the held-out split leaks — repeats of the same verdict act land on both folds, so verdict held-out ECE 0.141-0.212 is a within-act label-disagreement artifact, not miscalibration"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-split-leaks-repeats

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
