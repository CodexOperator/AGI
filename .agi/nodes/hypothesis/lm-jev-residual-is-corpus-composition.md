---
id: hypothesis:lm-jev-residual-is-corpus-composition
mint_id: 2653523d61094c8c909cbfc765466fd7
type: hypothesis
parents:
  - idea:lm-why-jev-echoes-leaked-verdicts
  - goal:g14
next_edges: []
ceiling: <= 1 USD OpenRouter (parent+kid); 0 API calls; 0 compute; no downloads on ARM4C without an owner yes; runs <= 10 min
edited_by: brainstorm
falsifier: Per-kind kind-prior accuracy is at or below the 0.507 global base for BOTH kinds (no composition effect) AND jev scrubbed agreement exceeds each kind-prior on that kind (then the residual is real reading, not composition, and H4/H5 carry the explanation instead).
scaffold_hash: 86afb3c861f3c1cc
season: 2
testable_claim: "On the pinned 370-act corpus, a body-blind classifier that predicts each act the majority verdict class of its KIND (verdict vs experiment) scores 0.615 pooled (measured: verdict majority inconclusive_lean_proved n=120/169; experiment majority proved n=107/200). Claim: pooled jev scrubbed q1 (0.588 to 0.596) is BELOW this body-blind prior, so the pooled residual above chance is corpus composition, not body reading. And jev is genuinely better than the kind-prior on experiment acts (0.695 vs 0.535) but worse on verdict acts (0.479 vs 0.710), so the two populations must be scored separately or not at all. Report pooled kind-prior, per-kind prior, per-kind jev agreement, and the difference with a bootstrap CI over act ids."
tests: ONE pi parent + ONE kid, ARM4C-light slot (pure Python/NumPy, CPU, no network); steps (1) rebuild the pinned 370-act corpus labels from acts_replay_scrub.jsonl and node frontmatter; (2) compute per-kind majority and pooled kind-only accuracy, jev per-kind agreement from json_cache_scrub, and a 1000-resample bootstrap CI; (3) write the table and state whether pooled jev is above or below the kind-prior; rows to bench/<utc>.jsonl, kid persists rows after every probe, parent commits promptly, FILE SCOPE .agi/context/local-maxxing/typesafe/, anonymization rule (hosts/IPs/GPU models/locations/key ids never; aliases ARM4C GPU2070S CPU8G EDGE), kid line_ceiling 120
title: "WHY jev echoes, hop 5 (anything better, COMPOSITION): the surviving 0.081 is not signal -- a body-blind per-kind majority scores 0.615 pooled, ABOVE jev scrubbed 0.588, because the corpus is two populations (experiment 0.695 vs kind-prior 0.535; verdict 0.479 vs kind-prior 0.710)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-residual-is-corpus-composition

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
