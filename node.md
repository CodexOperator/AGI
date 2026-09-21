---
id: hypothesis:l3-node-without-mint-id
mint_id: 18743d9edf0344a7b8621bc8c8d16aa3
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-III
scaffold_hash: 906d4691a7d2e55a
season: 2
testable_claim: cli.py done (and a write.py repair verb for the parent) assigns a first mint_id to a kid node that carries none, keyed from the iteration manifest, so grid.py commit --all versions it with 0 errors; assigning a mint_id to a node that already has one stays refused.
thought_session: L3.19
title: A node minted outside node_writer gets its first mint_id from the manifest, not from a hand
---
<!-- BODY:BEGIN -->
# hypothesis:l3-node-without-mint-id

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OBSERVED 2026-09-07 12:15 UTC (Belam III, wave-3 cycle 2 landing): experiment:a00-230456c1-1abcda was written by the ladder's DeepSeek kid with its own file tool (edited_by: ubuntu, no mint_id, no scaffold_hash). grid.py commit --all now prints ERROR ... has no mint_id and refuses to version it on every grid_sync tick, and write.py refuses set mint_id by design (goal:g2.5: identity is assigned once, never by a verb). Nothing in the engine can adopt the node. FIX SHAPE: (1) cli.py done repairs a missing mint_id the way L3.15 made it repair a broken frontmatter block — mint through node_writer, stamp scaffold_hash, log the final bytes for the write-guard; (2) a parent-facing repair, write.py <id> adopt or cli.py repair <iter> <agent>, that does the same for a node the kid left behind, refusing when a mint_id already exists; (3) a red-first test for each, plus the live proof: run the repair on experiment:a00-230456c1-1abcda and show grid.py commit --all at 0 errors. FILES: extensions/agi/bin/cli.py :: done, extensions/agi/bin/node_writer.py :: mint id helper, extensions/agi/bin/write.py :: verb table, extensions/agi/bin/grid.py :: the refusal message, tests under extensions/agi/tests/. NOT IN SCOPE: the kid brief wording that tells kids to edit below the frontmatter (l3-done-broken-frontmatter owns it).
