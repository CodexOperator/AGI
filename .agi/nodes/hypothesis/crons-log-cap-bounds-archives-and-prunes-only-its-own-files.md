---
id: hypothesis:crons-log-cap-bounds-archives-and-prunes-only-its-own-files
mint_id: a3b8c8e09c2d40ffb921145d29169329
type: hypothesis
parents:
  - goal:g1
  - hypothesis:pass8-0926-residue-batch
next_edges: []
edited_by: belam
scaffold_hash: 07ee5e1eccfa709a
season: 2
testable_claim: "After one crons.py apply no managed log, base or archive, exceeds logs.cap_mb; enforce_log_caps touches only names this project declares, never other files in the shared ~/logs; and crons_live: false stops it."
thought_session: belam-S2-L5-IX
title: "the log cap bounds every archive and prunes only this project's own logs (assigned: director-engine)"
town: core
---
# hypothesis:crons-log-cap-bounds-archives-and-prunes-only-its-own-files

# the log cap bounds every archive and prunes only this project's own logs

## Measured (PASS 8: engine-delta-1 DEMOTE + cron-layer round, 5 of 8 stand)
- crons.py:482-494: a name matching _ARCHIVE_RE hits `continue` before the size test at :495 -- logs.cap_mb=16 is a rotation trigger, not a cap; 172 MB above it persists, live on this box.
- crons.py:489-493: the _NESTED_RE branch unlinks before any size check on every unprompted apply.
- crons.py:1072: enforce_log_caps runs outside the crons_live branch (:1060-1065), so the kill switch does not stop it.
- crons.py:478-479: the glob enumerates the whole shared ~/logs (sanctuary-guard/, other services), not this project's declared names.

## Falsifiers
- after one apply, any managed base or archive above logs.cap_mb; any file outside this project's declared names touched; any cap action with crons_live: false.

## Agent Notes
assigned: director-engine (PASS 8 residue, belam-S2-L5-IX 09-26; runs mur-p8chunk{1..15}of15)
