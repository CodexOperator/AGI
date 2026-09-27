---
id: hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write
mint_id: 0b764207c4494a45a5d167b539c75524
type: hypothesis
parents:
  - goal:g4.18.1.4
next_edges: []
confidence: 0.8
edited_by: director-engine
scaffold_hash: 8b25e9228029f4e9
season: 2
tags:
  - engine
  - write
  - node_writer
  - g4.18.1
testable_claim: "(1) a same-directory payload_ref change renames the file and the row in one write, mint_id unchanged (2) a cross-directory or cross-location change is refused unless explicitly confirmed (3) the row always resolves to an existing file and an existing destination is never overwritten (assigned: director-engine)"
title: "a payload_ref change renames the file in the same write; a directory move needs an explicit confirm (goal:g4.18.1.4; assigned: director-engine)"
town: core
---
# hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write

## Measured
- A build node names its file by `payload_ref` + `location` (a base NAME, locations.payload_base, locations.py:445). A write that sets `location` in the same edit wins over disk (write.py ~2218-2221), but NOTHING moves the file: `grep -nE 'git mv|shutil.move|rename\('` over write.py + node_writer.py = 0 hits (`os.replace` only for atomic temp writes, node_writer.py:1127, :1203). So `set payload_ref=<new>` rewrites the row and leaves the file at the old name: the row dangles until a hand `git mv`.

## CLAIM
(1) a node write that changes `payload_ref` to a new NAME in the same directory renames the file and updates the row in ONE write (mint_id unchanged, the grid history of the node continuous) (2) a change that moves the file to another DIRECTORY or another `location` is REFUSED, naming both paths, unless the write carries an explicit confirm (one named flag/verb arg); with it, the move happens (3) after any such write the row resolves to an existing file, the old path no longer exists, and an existing file at the destination is refused (never overwritten).

## Dispatch line
config-max: none (bases are already config names). template-max: none. code: the rename path in the writer, because no mover exists.

## FALSIFIERS
- a same-dir rename on a temp build node leaves the old file or a dangling row, or changes mint_id.
- a cross-directory change without the confirm moves any byte.
- a rename onto an existing file overwrites it.

## TESTS
extensions/agi/tests/test_payload_rename.py (new; temp graph under tmp_path only). Neighbourhood: test_write*.py test_node_writer*.py test_links*.py. Every pytest under `timeout 600`, --basetemp under /tmp.

## FILE SCOPE
extensions/agi/bin/node_writer.py (a mover beside replace_payload) · extensions/agi/bin/write.py (ONLY the update path that calls it, ~2215-2250 -- never main()/create/answers: goal:g4.18.1.1 is under review there) · extensions/agi/tests/test_payload_rename.py.

## CEILING
1-2 kids · <= 45 production lines · pi-free tier-0 · 0 USD. No test spawns pytest; kids never launch real claude.
