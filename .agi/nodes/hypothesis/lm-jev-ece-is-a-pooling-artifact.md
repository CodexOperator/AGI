---
id: hypothesis:lm-jev-ece-is-a-pooling-artifact
mint_id: 9593a01b6b94404ba4c064bdf3fc1ec9
type: hypothesis
parents:
  - idea:lm-why-jev-echoes-leaked-verdicts
  - goal:g14
next_edges: []
ceiling: <= 1 USD OpenRouter (parent+kid); 0 API calls (cached probabilities only); 0 compute; no downloads on ARM4C without an owner yes; runs <= 10 min
edited_by: brainstorm
falsifier: Verdict-subgroup held-out ECE stays above 0.10 after per-group fitting (the miscalibration is not a temperature/pooling problem and the confidence carries no usable group-level signal) OR per-group fitting moves argmax agreement by more than 0.02 (the split or the fit is broken) OR experiment-subgroup ECE rises above 0.10 after fitting (overfitting).
scaffold_hash: 48a4c540e3067c4a
season: 2
testable_claim: "Recompute from the cached probabilities only (json_cache_scrub, 0 new API calls): pooled q1 ECE is 0.152 and splits into experiment 0.078 (n=200) and verdict 0.326 (n=169). Claim: grouping is the whole story. Fit ONE temperature per subgroup (experiment, verdict) on a 50/50 held-out split by act id, using the cached q1 probabilities; on the held-out fold BOTH subgroup ECEs fall to <= 0.10, and pooled ECE after per-group fitting also falls to <= 0.12. Argmax q1 agreement is unchanged within +/- 0.02 (temperature cannot change argmax). Report ECE by subgroup before and after, pooled before and after, and the fitted temperatures."
tests: ONE pi parent + ONE kid, ARM4C-light slot (pure NumPy, CPU, no network, no GPU); steps (1) load json_cache_scrub q1 probabilities and acts_replay_scrub.jsonl labels, rebuild per-act mean-probability distributions; (2) split act ids 50/50 by seed, fit one temperature per subgroup by NLL on the train fold, evaluate ECE on the held-out fold; (3) report the table and the fitted temperatures; rows to bench/<utc>.jsonl, kid persists rows after every probe, parent commits promptly, FILE SCOPE .agi/context/local-maxxing/typesafe/, anonymization rule (hosts/IPs/GPU models/locations/key ids never; aliases ARM4C GPU2070S CPU8G EDGE), kid line_ceiling 120
title: "WHY jev echoes, hop 4 (cause 4, CALIBRATION): the pooled ECE 0.196 is a per-group pooling artifact -- experiment acts already calibrate at ECE 0.078 while verdict acts sit at 0.326, so a per-group temperature fit on a held-out fold brings BOTH under 0.10 with argmax unchanged"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-ece-is-a-pooling-artifact

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
