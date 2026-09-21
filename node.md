---
id: hypothesis:lm-jev-verdict-ece-floor-is-label-disagreement
mint_id: f454018a08a042fdb647aa9bc315acf4
type: hypothesis
parents:
  - idea:lm-why-verdict-ece-ignores-temperature
next_edges: []
edited_by: thought-master
scaffold_hash: 1de58b3f2d792b91
season: 2
testable_claim: "On the committed q1 rows (json_cache_scrub + acts_replay_scrub.jsonl, 0 API calls), the TM.57 50/50 by-act-id split and 5 seeds (20260918/1/7/42/1234), splitting VERDICT acts by 3-repeat label agreement into unanimous (3/3 same q1 label) and contested: (i) a per-group temperature fit by NLL on the train fold, evaluated on the unanimous held-out subset only, reaches ECE <= 0.10 on >= 4/5 seeds, and (ii) the contested held-out subset stays > 0.10 on >= 4/5 seeds under both temperature and per-group isotonic (PAVA, TM.73 code); report the contested fraction of verdict acts (TM.54 predicts ~20 pct) and the unanimous-subset row count per seed; falsifier: unanimous-subset held-out ECE > 0.10 on >= 2/5 seeds -- then the residual is not label disagreement and cause 4 (refit on the self-reported scalar, channel A, acts_replay.py:139) is the next hop; 0 USD compute, ARM4C-light numpy or CPU8G, cap 1 USD pi"
title: "WHY hop 6f (after 6d scale and 6e shape both failed): the verdict-subgroup held-out ECE floor is LABEL DISAGREEMENT -- on verdict acts whose 3 repeats agree unanimously, one temperature reaches held-out ECE <= 0.10; the contested acts set the floor"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-verdict-ece-floor-is-label-disagreement

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
