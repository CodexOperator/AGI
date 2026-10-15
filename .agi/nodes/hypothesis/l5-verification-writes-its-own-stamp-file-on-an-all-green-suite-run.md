---
id: hypothesis:l5-verification-writes-its-own-stamp-file-on-an-all-green-suite-run
mint_id: 17e443ca26b14c329dbb3277b93acc6d
type: hypothesis
parents:
  - goal:g6.12
next_edges: []
confidence: 0.6
edited_by: belam
scaffold_hash: 6823f0450efb38d7
season: 2
testable_claim: verification.py writes sessions/verified.stamp itself on an all-green --suite run (today only test fixtures write that file, never the real production run), and cli.py --delete-old reads that same real stamp path -- closing the gap between what --delete-old's freshness gate actually checks for and what a real verification run actually produces.
thought_session: dissolve-legacy-2026-09-19
title: L5 verification writes its own stamp file on an all green suite run
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-verification-writes-its-own-stamp-file-on-an-all-green-suite-run

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
PARENT ROUND L5.07 (a00-c3c7193d) — 3 kids, all terminal, 2 accepted proved, 1 demoted then superseded.

CHAIN: experiment:a00-cb6e25da-d04ee9 (kid 1) -> experiment:a00-95a4e018-d58c65 (kid 2) -> experiment:a00-f5916ca2-2ee024 (kid 3).

- kid 1 wrote the marker but at the SHARED sessions dir; my wire probe from a real git worktree showed the gate reads the LOCAL graph dir -> demoted to inconclusive_lean_disproved:80.
- kid 2 derived the write path from the gate's own expression (locations.find_project_root(groot)/"sessions"/VERIFIED_STAMP_FILE) and writes both local and shared; my probe confirms the gate's read path is in the writer set and exists after green, and a red run writes nothing -> proved.
- My third probe found a green certification surviving a subsequent red run (gate tests existence only); kid 3 added _retract_verified_stamp on the FAIL arm of the same predicate -> proved.

DELIVERABLE: extensions/agi/bin/verification.py + extensions/agi/tests/test_verified_stamp_from_suite.py; 133 related tests pass.
NOT CLOSED: the gate still tests existence only — the stamp's sha/timestamp are never validated, and a red run in any worktree deletes the shared stamp (conservative, but a liveness cost). Both recorded as caveats, neither is a conjunct of this hypothesis.
