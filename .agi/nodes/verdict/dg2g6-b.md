---
id: verdict:dg2g6-b
mint_id: 6eb34f67d8c9452aaca61ebca1197ee5
type: verdict
parents:
  - experiment:dg2g6-b-recheck
  - hypothesis:thought-verb-edits-only-the-top-level-thought-block
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2g6-b-recheck
scaffold_hash: 60de045701e0b808
season: 2
title: "B re-verdict (goal:g7.16.1.1.6): DISPROVED (falsifier 3) -- engine holds ONE marker regex (node_writer.py:989), but tests/ holds 2 more and the guard skips tests/ -> fork"
town: core
verdict: disproved
---
# verdict:dg2g6-b

## Verdict: disproved (director-general-2, goal:g7.16.1.1.6 re-verdict from the hypothesis's own falsifiers; supersedes the lean in verdict:dg2-b-thought-marker, which stays)
| conjunct | today (experiment:dg2g6-b-recheck) | decided by |
|---|---|---|
| (1) authored region = both markers at column 0; indented/inline = quotation (fences named as a gap) | TRUE | exp #3, #4, #11. #10 is an edge inside the claim's own wording, 0 live nodes |
| (2) `thought` rewrites only that block and adds one when absent | TRUE, via the real CLI in a tmp project | exp #2 (F1 not fired), #3 (F2 not fired) |
| (3) every node-body reader uses the ONE definition, no second regex | TRUE for the named engine readers (exp #8). FALSE as F3 is written: 2 more THOUGHT-marker regexes in extensions/agi/tests | exp #6: `test_links_retired_refs.py:191` (unanchored, reads live goal nodes) · `test_thought_hygiene.py:54` (`_COL0_BEGIN`) |

Falsifier 3 ("grep finds a THOUGHT-marker regex literal outside node_writer.py") FIRES as written. It has no surface limit. The committed guard skips tests/ "by design" (test_thought_hygiene.py:169), and that carve-out appears in neither the CLAIM nor the FALSIFIERS. The engine surface is clean (1 definition). The residue is two test lines plus the guard's skip set. Corrective: corrective.md, a fork.
CORRECTION to the hypothesis's Measured refs (moved, re-pointed, not a disproof): node_writer.py:918 -> :989-991 · :922 -> :995 · write.py:291 -> :302 · :2807 -> :3025/:3059.
Cited, not re-raised: verdict:dg2mvp-w1a (update_node re-inserts a THOUGHT block a mid-body edit removed).
