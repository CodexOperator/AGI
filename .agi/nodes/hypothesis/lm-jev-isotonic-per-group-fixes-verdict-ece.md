---
id: hypothesis:lm-jev-isotonic-per-group-fixes-verdict-ece
mint_id: 5b78914b8b8647c0b24547946de0e966
type: hypothesis
parents:
  - idea:lm-why-verdict-ece-ignores-temperature
next_edges: []
edited_by: thought-master
scaffold_hash: 59372a06b5acac2a
season: 2
testable_claim: On the committed q1 rows (json_cache_scrub + acts_replay_scrub.jsonl, 0 API calls), the same 50/50 by-act-id split and 5 seeds (20260918/1/7/42/1234) as experiment:a00-bdec620b-6c4cf7, per-group isotonic regression of top-1 confidence against top-1 correctness fit on the train fold brings verdict-subgroup held-out ECE from 0.141-0.212 to <= 0.10 on >= 4/5 seeds while experiment-subgroup held-out ECE stays <= 0.12; if verdict held-out ECE stays > 0.10 under isotonic the residual is neither scale nor shape and the next lever is the 3-repeat agreement split (cause 3) or the elicitation channel A vs B (cause 4)
title: "WHY hop 6e: the verdict residual is SHAPE not scale -- per-group isotonic regression fit on the held-out train fold brings verdict held-out ECE <= 0.10 where one temperature left 0.141-0.212"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-isotonic-per-group-fixes-verdict-ece

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
