---
id: hypothesis:l5-verification-writes-its-own-stamp-file-on-an-all-green-suite-run
mint_id: 17e443ca26b14c329dbb3277b93acc6d
type: hypothesis
parents:
  - goal:g15
next_edges: []
confidence: 0.6
edited_by: sanctuary-director
scaffold_hash: 6823f0450efb38d7
season: 2
testable_claim: verification.py writes sessions/verified.stamp itself on an all-green --suite run (today only test fixtures write that file, never the real production run), and cli.py --delete-old reads that same real stamp path -- closing the gap between what --delete-old's freshness gate actually checks for and what a real verification run actually produces.
title: L5 verification writes its own stamp file on an all green suite run
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-verification-writes-its-own-stamp-file-on-an-all-green-suite-run

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
