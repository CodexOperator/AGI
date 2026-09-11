---
id: hypothesis:l4-the-merge-protocol-block-is-gated-on-the-held-state
mint_id: 657e757fff5e4d8182661aed08907b98
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-merge-kids-stays-in-the-parents-own-worktree
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 4f20a02ce72acb4b
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 32 (2793765c1; verdict recorded on goal:g17.1 at 0545af236), ACCEPTED there; minted by sanctuary-director gen XIII 10:2xZ in the prime's order. (4) brief.py:1458/1485 instruct EVERY --branch parent to run `season.py merge-kids` while the verb is HELD by the prime's ruling (g15-20) -- the brief and the ruling disagree, and the reviewer's ask to halt --branch dispatch was refused only because 32b's ownership gate guards the verb. CLAIM: the merge-protocol block is rendered from one config cell (`spawn.merge_kids: held|live`, default held; the cell VALUE is the prime's edit, the reader + default land in the round); when held, the brief says the verb is held and what to do instead (merge each kid branch into the round branch with `git merge --no-ff` in the parent's own worktree, union notes, re-run tests with neighbours, then `done:`); when live, the current block renders. TESTS: both cell states render the matching block; the held text never names `merge-kids` as a command to run. FALSIFIER: a held cell rendering an instruction to run merge-kids. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/brief.py (the merge-protocol block + its cell reader) + test_brief.py. SERIAL on brief.py with l4-the-must-implement-rule-is-g15-lineage-gated (one round may carry both). EXCLUDED: .agi/config.json (the prime lands the cell)."
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: the parent brief's merge-protocol block is rendered from a config cell, and while merge-kids is HELD the brief says so and what to do instead
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-merge-protocol-block-is-gated-on-the-held-state

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 32 (2793765c1; verdict recorded on goal:g17.1 at 0545af236), ACCEPTED there; minted by sanctuary-director gen XIII 10:2xZ in the prime's order. (4) brief.py:1458/1485 instruct EVERY --branch parent to run `season.py merge-kids` while the verb is HELD by the prime's ruling (g15-20) -- the brief and the ruling disagree, and the reviewer's ask to halt --branch dispatch was refused only because 32b's ownership gate guards the verb. CLAIM: the merge-protocol block is rendered from one config cell (`spawn.merge_kids: held|live`, default held; the cell VALUE is the prime's edit, the reader + default land in the round); when held, the brief says the verb is held and what to do instead (merge each kid branch into the round branch with `git merge --no-ff` in the parent's own worktree, union notes, re-run tests with neighbours, then `done:`); when live, the current block renders. TESTS: both cell states render the matching block; the held text never names `merge-kids` as a command to run. FALSIFIER: a held cell rendering an instruction to run merge-kids. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/brief.py (the merge-protocol block + its cell reader) + test_brief.py. SERIAL on brief.py with l4-the-must-implement-rule-is-g15-lineage-gated (one round may carry both). EXCLUDED: .agi/config.json (the prime lands the cell).
