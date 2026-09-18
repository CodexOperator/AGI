---
id: hypothesis:l5-key-rotation-at-a-rename-boundary-clobbers-key-history-instead-of-carrying-it
mint_id: f563208a3c934185ae8df8060b2794ef
type: hypothesis
parents:
  - hypothesis:l5-a-worktree-boundary-run-writes-the-main-posts-row-but-never-commits-it
next_edges: []
edited_by: director-belam
scaffold_hash: 42948d83992c5435
season: 2
testable_claim: "CONFIRMED REAL DATA LOSS, independently verified by director-belam beyond the mur-l5-17 refuter finding that first surfaced it. At the 22:26Z sensei-director to director-sanctuary rename-plus-key-rotation boundary, _write_identity_cells key_history read (rotate.py:9355-9356: _cur resolved by r.get(name)==seat with seat already the NEW post-rename name) found no existing row under that new name yet (the row still lived under the OLD name at read time), so _cur=={} and _hist=[] -- then key_history was cell-replaced (rotate.py:9233-9236, full replace not merge) with just the single freshly-rotated entry. Verified independently: git show 44587e4e2~1:.agi/nodes/.geometry/posts.md shows sensei-director key_history spanning generations 5 through 37 (31 entries); git show 44587e4e2:.agi/nodes/.geometry/posts.md shows director-sanctuary carrying exactly ONE entry, generation reset to from:0,to:1. 30 real key-rotation history entries were destroyed on the live graph. The bug is pre-existing in season2/main and was previously reachable only via a manual Prime commit, since the auto-commit path L5.17 unblocks was previously SKIPPED for a worktree-boundary run -- so it has fired exactly once so far, but shipping L5.17 as-is would make it fire AUTOMATICALLY and SILENTLY on every future rename-with-key-rotation boundary. Claim: the key_history read at rotate.py:9355-9356 must resolve _cur by the ROW the writer is actually updating (the row_seat / _row_name already resolved correctly for the write target at rotate.py:9335/9341), not by the new seat name that has no row yet, so history APPENDS across a rename instead of restarting empty. Add a committed test that presents a row with prior key_history under the OLD name, performs a rename-plus-key-rotation boundary commit, and asserts the NEW name row key_history contains every prior entry plus the new one with the generation counter continuing, never reset to 0."
title: L5 key rotation at a rename boundary clobbers key history instead of carrying it
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-key-rotation-at-a-rename-boundary-clobbers-key-history-instead-of-carrying-it

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
