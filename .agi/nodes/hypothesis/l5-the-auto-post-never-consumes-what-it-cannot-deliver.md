---
id: hypothesis:l5-the-auto-post-never-consumes-what-it-cannot-deliver
mint_id: 9e6ac05d5bf849a1bdee103f3bada205
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
confidence: 0.7
edited_by: belam
scaffold_hash: 57cb0a91c1e530da
season: 2
testable_claim: (a) _run_send_read reports a timeout or an empty body as NOT delivered -- the inbox marker is left untouched and the hook prints one undelivered line, never DELIVERED + the F25 suppression; (b) _auto_post runs AFTER the existing fail-closed required-field gate, so a turn missing transcript_path never consumes the inbox; (c) committed fixtures exist for the byte-cap truncate branch and the NO_SPAWN decline branch (both previously covered only by scratch probes).
thought_session: dissolve-legacy-2026-09-19
title: L5 the auto post never consumes what it cannot deliver
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-the-auto-post-never-consumes-what-it-cannot-deliver

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
