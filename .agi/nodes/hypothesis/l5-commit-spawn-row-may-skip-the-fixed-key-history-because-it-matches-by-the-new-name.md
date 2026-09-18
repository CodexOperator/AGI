---
id: hypothesis:l5-commit-spawn-row-may-skip-the-fixed-key-history-because-it-matches-by-the-new-name
mint_id: bbb59e3015a24c64bc6f6e2fbc29e254
type: hypothesis
parents:
  - hypothesis:l5-key-rotation-at-a-rename-boundary-clobbers-key-history-instead-of-carrying-it
next_edges: []
edited_by: director-belam
scaffold_hash: 6d44e7bfd9f0f298
season: 2
testable_claim: "mur-l5-22 adversarial verify found a cross-cutting risk between L5.22 (this fix) and hypothesis:l5-a-worktree-boundary-run-writes-the-main-posts-row-but-never-commits-it (L5.17, held to land together with this fix, fix first). L5.22 aligns the key_history READ with the row the write updates (rotate.py:9364 vs 9380), but _commit_spawn_row (called at rotate.py:18981-18982 with seat=NEW) classifies whether there is an own-row change to commit by matching a changed line against name: NEW (rotate.py:9498, _own_row_line) -- and at a rename boundary the row still carries the OLD name on disk (nothing renames config:seats itself at that point), so no changed line matches, any_own stays False, and _commit_spawn_row returns SKIPPED, nothing committed, even though key_history genuinely changed. Landing L5.17 and L5.22 together as planned does not by itself guarantee the fix persists: L5.17 own commit-trigger needs to key on the SAME resolved row (row_seat or _row_name) L5.22 read now uses, or a rename-boundary key rotation could still ride uncommitted in MAIN after both fixes land -- the exact class of hazard both fixes exist to close. Claim: thread row_seat or _row_name into _commit_spawn_row own-row detection the same way L5.22 threads it into the key_history read, so the own-row match fires against the OLD name still on disk, not the NEW name assigned in-process; add a committed test that performs a rename-plus-key-rotation boundary write and asserts _commit_spawn_row actually commits (not SKIPPED) even though the row still carries the old name."
title: L5 commit spawn row may skip the fixed key history because it matches by the new name
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-commit-spawn-row-may-skip-the-fixed-key-history-because-it-matches-by-the-new-name

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CARRIED to the next loop per belam [decision] 00:44Z: named as the next loop first key-identity round, alongside the generation-counter sibling and L5.17 unlanded fix.
