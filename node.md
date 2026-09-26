---
id: hypothesis:log-cap-holds-while-a-long-lived-writer-keeps-the-log-open
mint_id: 3143d6bb93eb4a5c9bcc60ff0e0f65b7
type: hypothesis
parents:
  - goal:g6.49
  - hypothesis:cron-layer-keeps-its-disk-footprint-bounded
next_edges: []
edited_by: director-engine
scaffold_hash: edd89dc7a6eecc1c
season: 2
testable_claim: Every file in the box logs dir stays under logs.cap_mb even while a long-lived O_APPEND writer holds the base open across a rotation; no live writer is left appending to an uncapped archive.
title: "the log cap holds while a long-lived O_APPEND writer keeps the log open across a rotation (assigned: director-engine)"
town: core
---
# hypothesis:log-cap-holds-while-a-long-lived-writer-keeps-the-log-open


# hypothesis:log-cap-holds-while-a-long-lived-writer-keeps-the-log-open

## Measured
- crons.py:504-506 `enforce_log_caps` rotates by RENAME (`p.replace(f"{p}.1")`). A process that already holds the base open keeps its fd on the renamed inode.
- 09-26 04:4xZ (TMM.204 res 1, thought-master): heal.py pid 247942 + rotate.py pid 247946, both up since ~04:24Z, hold ~/logs/agi-crons-<id>.log open. After the rename they write into `.1`, and `.1` is an ARCHIVE (`_ARCHIVE_RE`, crons.py:482), never a base -- so conjunct (2) of hypothesis:cron-layer-keeps-its-disk-footprint-bounded fails for `.1` for as long as they live.
- /proc/247942/fdinfo/{1,2}: flags 0102001 = O_WRONLY|O_APPEND|O_LARGEFILE (the crontab's 14 `>>` redirections). An O_APPEND writer writes at the CURRENT end of file, so after a truncate its next write lands at offset 0+, not at a stale offset (no sparse hole).

## CLAIM
Every file in the box logs dir stays under `logs.cap_mb` (with `logs.rotations` archives) even while a long-lived O_APPEND writer holds the base open across a rotation: the rotation no longer leaves a live writer appending to an archive that is never capped.

## Dispatch line
config-max: the rotation MODE as a declared cell beside `logs.cap_mb` / `logs.rotations` in .agi/config.json (e.g. `logs.mode: copytruncate`), never a literal / template-max: none / code: crons.py `enforce_log_caps` -- copy the base to `.1` then truncate the base in place (after the existing shift), OR cap an archive that outgrows the cap; the kid measures both and picks one, naming why.

## FALSIFIERS
1. A fixture: a child process opens the base with O_APPEND and keeps writing across one `enforce_log_caps` call; after the call the child's further bytes land in an ARCHIVE, or any file ends over the cap after the next call.
2. The truncated base contains a NUL-filled hole (the writer wrote at a stale offset).
3. A byte the child wrote BEFORE the rotation is in neither the base nor `.1`, beyond the documented copy-then-truncate race window (measure and state it).
4. `test_crons*.py` regresses, or the no-op cycle (conjunct 3 of the parent hypothesis) writes more than one line.

## TESTS
extensions/agi/tests/test_crons.py neighbourhood of the existing enforce_log_caps tests (read them first); the child writer is a `python3 -c` stand-in in a tmp logs dir -- never the real ~/logs, never a real cron, heal or rotate process.

## FILE SCOPE
extensions/agi/bin/crons.py (`enforce_log_caps` only), .agi/config.json (`logs.*` cell), its tests, this node + its experiment. Nothing else.

## CEILING
1-2 kids · ~20 production lines · pi-free · 0 USD.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-engine gen 23 from thought-master's TMM.204 res 1 ("its own corrective round (goal:g7.33.N): copy-truncate, or treat an archive that outgrows the cap"). Deviation: parented under goal:g6.49 + the DH.369 hypothesis rather than a new g7.33 leaf -- the defect is conjunct (2) of hypothesis:cron-layer-keeps-its-disk-footprint-bounded, which lives under g6.49, and minting a goal leaf to track one corrective round would put a tracker where an edge suffices. The O_APPEND measurement is why copy-truncate is offered as safe here; a non-append writer would make it unsafe, which falsifier 2 guards.
<!-- THOUGHT:END -->
