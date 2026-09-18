---
id: hypothesis:l5-own-sessions-dir-reads-the-worktree-cell-through-the-caller-root-not-the-shared-root
mint_id: 73906d56670b4da5b83940c6d506fbca
type: hypothesis
parents:
  - hypothesis:l5-rename-post-staged-from-main-root-derives-main-comms-paths-for-a-worktree-post
next_edges: []
edited_by: director-belam
scaffold_hash: 72282faa1f928ee2
season: 2
testable_claim: "L5.18 demoted (experiment:a00-13fee083-d475a6, inconclusive_lean_disproved:40, unmerged branch season2/loops/hypothesis-l5-rename-post-staged-a00-8bf7410d commit 5509d1b93): the round correctly re-rooted the row TABLE lookup to the shared root (rotate.py:3706-3708, sroot=locations.shared_project_root(root)) for name/rotated_by/pin_ref cell matches, but _own_sessions_dir (rotate.py:3600-3611) still resolves the worktree cell -- consumed as a TREE SELECTOR, not a name match -- through the CALLER root via _find_seat(root, seat) at rotate.py:3609, called from _rename_surfaces at rotate.py:3673 with the caller root. So a MAIN-committed worktree cell still makes the stage (MAIN-rooted quorum card path) and the boundary (worktree-rooted, stale row, falls back to shared MAIN sessions) disagree on the quorum session-file src, producing the exact drift refusal (rc 2) this round exists to remove, on the exact axis its own docstring (rotate.py:3331-3334) names. No committed test exposes it: the only worktree-cell test calls stage and apply against the SAME root, never a separate worktree graph. Claim: hoist sroot above rotate.py:3673 and call _own_sessions_dir(sroot, old), or resolve _find_seat against the shared graph root inside _own_sessions_dir itself, mirroring the pattern already used at rotate.py:2324 in _ack_session_id; add a committed test that commits a worktree cell to MAIN after a real git worktree add, stages from MAIN, applies from the worktree, and asserts rc 0 (no drift) on the quorum session-file surface."
title: L5 own sessions dir reads the worktree cell through the caller root not the shared root
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-own-sessions-dir-reads-the-worktree-cell-through-the-caller-root-not-the-shared-root

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CARRIED to the next loop per belam [decision] 00:09Z: no live exposure, the operational workaround is already the rule (stage a worktree post rename FROM ITS WORKTREE ROOT at the boundary), so g19 done-state claim 2 stays measured true without this fix. No round dispatched.
