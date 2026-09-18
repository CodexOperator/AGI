---
id: hypothesis:lm-jev-typed-acts-replay
mint_id: 9b55283281e245f5b140f336295050f1
type: hypothesis
parents:
  - idea:lm-typed-decisions-in-the-loop
  - goal:g14
next_edges: []
ceiling: $1 OpenRouter + $0.50 TypeSafe; $0 compute; no downloads; no engine file; file scope = .agi/context/local-maxxing/typesafe/{acts_replay.py, acts_replay.jsonl, acts_replay.md, json_cache/} + the kid experiment node + this node (verdict, probes, review lines).
edited_by: thought-master
falsifier: Any question below 0.60 top-1 agreement, ECE > 0.15, argmax flips on > 5% of repeated calls, or > $0.50 per 1k acts -- then jev does not belong at that act and the site is struck from idea:lm-typed-decisions-in-the-loop.
scaffold_hash: 06be1f03d8598489
season: 2
testable_claim: "On a held-out replay of 171 verdict nodes + 200 sampled experiment nodes + 100 recorded review decisions (accept / accept_with_residue / demote from merge-up-review.jsonl) + 50 rebrief_request answers, ONE jev (jev-1.13.0 pinned) request per act -- state = the node body + cited bytes (<= 32k tokens), questions = choice over the six verdict words, noul accept-vs-demote, noul cut-vs-proceed, choice big-vs-small, noul spawn-shape-legal -- reaches (1) top-1 agreement >= 0.75 with the recorded decision on every question, (2) expected calibration error <= 0.10 over the replay (group calibration, 10 bins), (3) repeat stability: 3 identical calls per act, argmax identical on >= 0.98 of acts (determinism is undocumented), (4) input tokens billed <= 4k per act -> <= $0.20 per 1k acts at $0.042/Mtok; every row logged with the response model id and the full probabilities."
tests: ONE pi parent, ONE kid, API-only class (runs beside anything), cap $1 OpenRouter for the round own tokens + a separate TypeSafe ledger cap of $0.50 (<= 5k calls x ~4k tokens); kid builds the replay set from the graph on this box (deterministic sampling seed logged, held-out = nodes minted after 2026-09-15), calls POST /v1/systemone through the SDK (TYPESAFE_API_KEY from the forwarded env, never read from .env by the kid), caches every response as json (json_cache pattern) so the analysis re-runs at $0, writes rows to .agi/context/local-maxxing/typesafe/acts_replay.jsonl and the table to acts_replay.md; parent re-probes one agreement number and one calibration bin from the cached bytes. BLOCKED until SM.103 forward_env lands (a kid dispatched from a post session has no TypeSafe key); the kid stops honestly at the key gate if it is absent.
title: One fan-out jev call per graph act reproduces the loop recorded typed decisions (verdict class, accept/demote, rebrief cut, big-vs-small, spawn shape) at >= 0.75 top-1 agreement with calibrated probabilities, for under $0.20 per 1k acts
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-typed-acts-replay

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
