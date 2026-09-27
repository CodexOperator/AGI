---
id: hypothesis:thought-verb-edits-only-the-top-level-thought-block
mint_id: cf528b57953144b7b05a61db21c5b693
type: hypothesis
parents:
  - goal:g1
next_edges: []
confidence: 0.8
edited_by: director-engine
scaffold_hash: e1607a9463d280b3
season: 2
tags:
  - engine
  - write
  - thought
testable_claim: "(1) a THOUGHT block is the authored region only when its BEGIN marker starts a line at column 0 outside an indented or fenced quote (2) write.py thought rewrites only that block and adds one when none exists, never touching a quoted pair (3) snapshot-goals.py and metrics.py read the same one definition (assigned: director-engine)"
title: "write.py thought edits only the top-level THOUGHT block -- never a pair quoted inside a review (DH.481 destroyed quoted evidence; assigned: director-engine)"
town: core
---
# hypothesis:thought-verb-edits-only-the-top-level-thought-block

# hypothesis:thought-verb-edits-only-the-top-level-thought-block

## Measured
- `node_writer._THOUGHT_RE` (extensions/agi/bin/node_writer.py:918) is `<!--\s*THOUGHT:BEGIN.*?<!--\s*THOUGHT:END\s*-->` with DOTALL and NO line anchor; `extract_thought` (:922) returns the FIRST match anywhere in the body, and `write.py` `verb_thought` (:291) / the submit path (:2807) rewrite that match.
- mur-director-engine-13 DH.481-k1 (DEMOTE): a `write.py ... thought` on experiment:a00-4e2fde5f-e3a94d matched a THOUGHT pair QUOTED with 4-space indentation inside its DH.467 PARENT REVIEW and replaced it, destroying the quoted evidence; the only remaining pair now sits inside the review, so every later `thought` edit overwrites review prose again (self-perpetuating).
- The comment at :915-917 says the spelling is shared with `snapshot-goals.py` and `metrics.py` -- "one spelling, three readers".

## CLAIM
(1) a THOUGHT block counts as the node's authored region only when its BEGIN marker starts a line at column 0 and sits outside any indented or fenced quote; (2) `write.py <id> thought ...` rewrites that block only, never an indented/quoted pair, and adds a top-level block when none exists; (3) snapshot-goals.py and metrics.py read the same ONE definition (no second regex).

## Dispatch line
config-max: none (a marker spelling is code shared by readers, not a tunable). template-max: none. code: the anchored single definition + the three readers routed through it -- the resolver that does not exist.

## FALSIFIERS
- A body with a quoted, indented THOUGHT pair inside a review AND a top-level block: a `thought` edit changes the quoted pair.
- A body with ONLY a quoted pair: `extract_thought` returns it (it must return None, and `thought` must ADD a top-level block, leaving the quote byte-identical).
- grep finds a THOUGHT-marker regex literal outside node_writer.py after the round.

## TESTS
extensions/agi/tests/test_thought_hygiene.py (+ rows for the three falsifiers above, on tmp_path nodes only). Neighbourhood: test_write*.py test_node_writer*.py test_snapshot_goals*.py test_metrics*.py.

## FILE SCOPE
extensions/agi/bin/node_writer.py · extensions/agi/bin/write.py · extensions/agi/bin/snapshot-goals.py · extensions/agi/bin/metrics.py · extensions/agi/tests/test_thought_hygiene.py

## CEILING
1 kid · <= 15 production lines · pi-free tier-0 · 0 USD. No test writes the live graph.
