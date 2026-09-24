---
id: experiment:a00-73020c7e-profile-link-write
mint_id: 5a0b3d2c1e4f6a7b8c9d0e1f2a3b4c5d
type: experiment
parents:
  - hypothesis:a00-73020c7e-6d0a68
next_edges: []
confidence: 0.95
edited_by: a00-555d7afb
evidence_runs:
  - experiment:a00-73020c7e-profile-link-write
line_ceiling: 40
loop: DH.256
model: stealth/space-bunny-alpha
probes: "wire: real-write.py-set-profile_ref-plus-note-created-standing-artifact; gate: directory-target-compound-write-exited-2-with-named-refusal-and-left-directory-intact"
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
Parent probes are recorded in frontmatter and in the authored review below.
Parent probes are recorded in frontmatter and in the authored review below.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Instruction said: a single write.py submission that sets profile_ref and adds standing text must project the post-submit graph bytes without a second projection command. Machine actually does: the reviewed write.py call site invokes profile_sync.sync_node after the named edits at write.py lines 2021-2048, and the focused test at test_profile_sync.py lines 75-83 drives the real CLI then compares the artifact to profile_sync.project. I independently built and ran the session probe: the compound command created the standing artifact, while a directory-target variant exited 2 with a named refusal. Near miss: accepting a merely non-empty file or testing profile_sync.project directly would satisfy the wording while missing the live write.py seam; the wire probe crosses the real CLI and checks produced bytes. No standing rule was deviated from; my first probe expected uppercase REFUSED although the engine emits lowercase refused, so I made the assertion case-insensitive.
<!-- THOUGHT:END -->
