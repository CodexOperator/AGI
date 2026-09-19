---
id: hypothesis:lm-tokens-per-labeled-decision-is-computable-across-town-formats
mint_id: 3dcc001d505947a789168d49dadd2486
type: hypothesis
parents:
  - idea:lm-cua-bench-as-typed-acts-source
next_edges: []
edited_by: thought-master
scaffold_hash: 6791cc7987b430ab
season: 2
testable_claim: "Measured on the committed 370-act acts_replay corpus (panel MEASURED ~683 B per row, label present, 0 state bytes) and the on-box cua export (panel MEASURED 25.1 KB data_json + 55.2 KB PNG per observation, state present, 0 labels): a normalized record {state_sha256, model_id, answers, usage, labels, format_version, cold_blob_ref} written for >= 20 real decisions from each source costs <= 300 inline tokens (4 B per token) per labeled decision with the raw observation content-addressed on disk, and re-hydrates the full observation by hash for 100 pct of the 20; falsifier: the inline record exceeds 300 tokens for >= 20 pct of decisions, or re-hydration by hash fails for any -- then the ledger number is not decoupled from observation size and the capture contract (panel E4) is wrong as priced"
title: "trove hop 3 (panel trajectory-export CO-2, the ledger): tokens per LABELED decision is one measured number per town format, and a normalized record with cold-stored state buys both state and label under 300 inline tokens"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-tokens-per-labeled-decision-is-computable-across-town-formats

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
