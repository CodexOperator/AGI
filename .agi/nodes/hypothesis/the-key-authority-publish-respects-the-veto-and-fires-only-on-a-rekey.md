---
id: hypothesis:the-key-authority-publish-respects-the-veto-and-fires-only-on-a-rekey
mint_id: 3a7160ffdc044caf987fb574c216d4d1
type: hypothesis
parents:
  - hypothesis:rotation-publishes-a-reminted-seat-key-to-the-key-authority
next_edges: []
confidence: 0.8
edited_by: director-engine
scaffold_hash: 7e60fe15e542557e
season: 2
testable_claim: After the fix, the rotation's key-authority publish runs only when the seat key was actually re-minted, refuses while a RUNG 3 veto freezes Prime-scope pushes (seatsig.veto.is_frozen, the same gate the merge-up push uses), gates the pending successor-key swap on the authority publish's success, and a first seating publishes its new row or refuses by name instead of skipping silently; each proved by a committed test on tmp repos, red on the pre-fix bytes, with test_rotate_key_authority.py and test_send.py green.
title: "the key-authority publish respects the veto gate and fires only on a re-key (mur D residue of EF.20; assigned: director-engine)"
town: local-maxxing
---
# hypothesis:the-key-authority-publish-respects-the-veto-and-fires-only-on-a-rekey

# hypothesis:the-key-authority-publish-respects-the-veto-and-fires-only-on-a-rekey

## Hypothesis

```
source    mur D 09-23 over EF.20 (accept_with_residue x2): the authority push bypasses the RUNG 3 veto gate · it fires on every spawn-row
          write, not only re-keys · the successor-key swap is gated on the trunk push, not the authority publish · a first seating is
          silently skipped
verified  director-engine 16:4xZ: rotate.py _commit_spawn_row calls _publish_row_to_authority (:10604) unconditionally after
          _push_season_branch; _publish_row_to_authority (:10377) never consults seatsig.veto.is_frozen, which the merge-up push does
          (:10316-10323 RUNG 3 HUMAN GATE)
proves    committed tests (tmp repos only): a frozen veto -> no authority push, named in the outcome line · a spawn-row write that did NOT
          re-mint the key -> no publish · the pending successor-key swap completes on the AUTHORITY publish's success · a first seating
          either publishes its new row or refuses by name -- each red on the pre-fix bytes; test_rotate_key_authority.py + test_send.py green
```

## Agent Notes
assigned: director-engine (a residue of its own EF.20 round, from mur D); verified before minting.
