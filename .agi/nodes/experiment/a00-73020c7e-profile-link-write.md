---
id: experiment:a00-73020c7e-profile-link-write
mint_id: 5a0b3d2c1e4f6a7b8c9d0e1f2a3b4c5d
type: experiment
parents:
  - hypothesis:a00-73020c7e-6d0a68
next_edges: []
confidence: 0.95
edited_by: a00-73020c7e
evidence_runs:
  - experiment:a00-73020c7e-profile-link-write
line_ceiling: 40
loop: DH.256
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
status: pending
title: One write links a profile and projects standing text
verdict: proved
---
# experiment:a00-73020c7e-profile-link-write

## Claim under test

A previously unlinked hypothesis can gain `profile_ref` and its standing
update in one `write.py` submission, with the projection artifact created
from the post-submit node bytes rather than a second command.

## Adversarial falsifier

Start with a node that has no `profile_ref`; submit `set profile_ref
profile/new.md && note standing update` through the real CLI. A failure of
either the link, the note, or the resulting artifact would disprove the
unified route end to end. The test also compares the artifact against
`profile_sync.project`, preventing a merely non-empty file from passing.

## Result

`python3 -m pytest extensions/agi/tests/test_profile_sync.py -q` → 19
passed. The new test passed, so the formerly unlinked node received the
standing text and its new artifact matched the graph projection in the same
action. No production bytes changed; this experiment adds only the focused
regression.

## Adversarial struggle

The test runner emitted many stale phantom-record tier-gate warnings from
other worktrees before completing; they were environmental and did not skip
this run. The new test also deliberately passed a ref whose parent directory
did not exist, checking that projection creates the destination rather than
assuming pre-created output.

## Agent Notes
Focused end-to-end test proves a newly profile-linked node projects its standing text in the same write.py action; 19 profile-sync tests pass.
