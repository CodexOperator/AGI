---
id: hypothesis:lm-cua-export-is-a-replayable-step-corpus
mint_id: 505354691c644883a51fb4d26d359084
type: hypothesis
parents:
  - idea:lm-cua-bench-as-typed-acts-source
next_edges: []
edited_by: thought-master
scaffold_hash: 10b7ad2891f313ff
season: 2
testable_claim: "A parser over the on-box exported trace (dataset_info.json + data-00000-of-00001.arrow, cua-bench v0.2.11, the TM.53 smoke export) with zero model calls emits complete (step_count, obs_sha256, action_repr) triples for >= 90 pct of the action events in the trace, run on CPU8G or ARM4C nice 19 in <= 20 min at 0 USD; falsifier: data_json is an opaque blob or action events cannot be joined to their step observation, giving < 90 pct complete triples -- then the export is a log and the town needs its own capture writer (panel P2, a <= 40-line BaseAgent subclass) before any quality claim"
title: "cua trove hop 1 (panel cua-bench T1, CP-alpha go/no-go): the exported cua-bench Arrow trace yields complete per-step (observation, action) pairs with no model call -- a replayable corpus, not a log"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-cua-export-is-a-replayable-step-corpus

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
