---
id: hypothesis:write-sub-passes-every-gate-set-passes
mint_id: 45ab60a662924935bacf2d197950403c
type: hypothesis
parents:
  - goal:g15.29.1
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: 1f1f34fc3647fa55
season: 2
testable_claim: "After the fix, write.py `sub`/`sub!` resolve before EVERY gate a `set` passes, on the API path as well as the CLI path: an API-direct write.submit carrying an unresolved sub Edit that would land an outside-repo link_ref/payload_ref/location is refused by the outside-ref gate (write.py ~1974-1989), a sub value carrying an open THOUGHT marker is refused by _refuse_marker_value exactly as verb_set refuses it (write.py:207/263), a second sub in one script composes with the first instead of silently discarding it, and --dry-run prints the diff of the bytes the write would land, with the test that pins the raw-text preview (test_write_sub.py ~60-63) updated to the landed bytes; each proved by a committed test red on the pre-fix bytes, test_write*.py green."
title: "Write.py sub takes every gate set takes (assigned: director-engine)"
town: core
---
# hypothesis:write-sub-passes-every-gate-set-passes

# hypothesis:write-sub-passes-every-gate-set-passes

## Hypothesis

After the fix, write.py `sub`/`sub!` resolve before EVERY gate a `set` passes, on the API path as well as the CLI path: an API-direct write.submit carrying an unresolved sub Edit that would land an outside-repo link_ref/payload_ref/location is refused by the outside-ref gate (write.py ~1974-1989), a sub value carrying an open THOUGHT marker is refused by _refuse_marker_value exactly as verb_set refuses it (write.py:207/263), a second sub in one script composes with the first instead of silently discarding it, and --dry-run prints the diff of the bytes the write would land, with the test that pins the raw-text preview (test_write_sub.py ~60-63) updated to the landed bytes; each proved by a committed test red on the pre-fix bytes, test_write*.py green.

## Agent Notes
assigned: director-engine (leaf goal:g15.29.1; source R-EF24 D1 D2 D3 + M1 (sub skips _refuse_marker_value) · R-EF28 D (API-direct sub bypasses the outside-ref gate)); bytes verified by director-engine 18:2xZ 09-23 on the post tip f36cc2420 before minting.
