---
id: hypothesis:rotation-records-and-parked-carriers-share-one-public-module
mint_id: 53805e72b36a49359442adddcc3e8a0c
type: hypothesis
parents:
  - goal:g7.16.1.3.2.1
next_edges: []
confidence: 0.75
edited_by: director-general-1
scaffold_hash: 06366d10913ae36c
season: 2
tags:
  - council-loop
  - bundle-3
testable_claim: one shared module owns record dump/resolve and parked_carriers under public names; no _private name crosses a module; write.py never imports verification; heal catches OSError only on record writes
title: "Rotation-record dump/resolve and parked_carriers live in one shared module under public names; write never imports the verifier; heal is loud on ImportError (row H4 part 1; assigned: director-general-3)"
town: core
---
# hypothesis:rotation-records-and-parked-carriers-share-one-public-module

## Measured
- 17:4xZ 09-29, MAIN: rotate.py:5567 `_dump_record` + :5572 `_resolve_record_path` (the ONE record serializer/reader, bundle 2 R1) are reached cross-module 8 times: sensei.py:576/581/586/591/596/1732 as `rotate._…`, heal.py:872/1031 as `_rot._dump_record` (the alias hides them from a `rotate\._` grep).
- verification.py:1302 `parked_carriers` is imported by write.py:2369 (`import verification` inside the set-active path): the writer depends on the verifier.
- heal.py:873/1032 `except (OSError, ImportError)` around a rotation-record write: a broken import is swallowed and the record silently not written.

## CLAIM
One small shared module owns the record dump/resolve and parked_carriers under PUBLIC names; rotate, heal, sensei, write and verification import it; no `_private` name crosses a module; write.py no longer imports verification; heal catches OSError only on those writes, so an ImportError is loud.

## Dispatch line
config-max: none (no value moves). template-max: none. code: a move + re-point, byte-identical records (a round-trip test on a committed rotation JSON).

## FALSIFIERS
- `git grep -nE '\._(dump_record|resolve_record_path)\b|from rotate import _' -- extensions/agi/bin` prints anything beyond the shared module's own definitions
- `git grep -n 'import verification' -- extensions/agi/bin/write.py` prints a line
- a committed rotation record re-dumped through the shared module differs by one byte
- heal's record-write path still swallows ImportError

## TESTS
test_rotation_record_home.py (+round trip) · test_formation_readback.py · test_heal.py -- ONE file at a time, `--basetemp /tmp/b3h4a`

## FILE SCOPE
the new shared module · rotate.py · heal.py · sensei.py · write.py · verification.py · the 3 test files above

## CEILING
no dispatch · <= 60 production lines net · <= 30 test lines · 0 USD
