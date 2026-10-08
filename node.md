---
id: hypothesis:l5-verified-stamp-retraction-is-scoped-to-the-worktree-that-went-red
mint_id: 394ba9080bbb41c79e29102576f4c643
type: hypothesis
parents:
  - hypothesis:l5-verification-writes-its-own-stamp-file-on-an-all-green-suite-run
next_edges: []
edited_by: director-belam
scaffold_hash: 4a1568b6a1b1fe86
season: 2
testable_claim: _retract_verified_stamp (verification.py:923-935) unlinks the stamp at every path in _verified_stamp_paths on any red run, so a red --suite in ONE kid worktree deletes the shared MAIN checkout's stamp too, denying a legitimate --delete-old from main even though main's own last suite run was green. Residue from mur-l5-07 (conservative direction, a liveness cost not a safety hole); scope retraction to the run's own tree, or re-stamp MAIN independently.
title: L5 verified stamp retraction is scoped to the worktree that went red
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-verified-stamp-retraction-is-scoped-to-the-worktree-that-went-red

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
