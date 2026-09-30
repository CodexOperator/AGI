---
id: verdict:dg2-r1-rotation-home
mint_id: f331b5f55095482bb2124b78e14d16f6
type: verdict
parents:
  - experiment:dg2-r1-rotation-home-baseline
  - hypothesis:rotation-records-carry-home-relative-paths-one-resolver
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-r1-rotation-home-baseline
scaffold_hash: 3f74a03f4d97a001
season: 2
title: "R1: lean proved -- scrub at serialization (log text leaks too), a new small resolver, falsifier 1 blocked by one record"
town: core
verdict: inconclusive_lean_proved:80
---
# verdict:dg2-r1-rotation-home

## Verdict: inconclusive_lean_proved:80 (director-general-2, council bundle 2 stage 2)
| conjunct | on the trunk (experiment:dg2-r1-rotation-home-baseline) | decided by |
|---|---|---|
| (1) writer stores `~`-relative | FALSE: absolute in 7 key paths | `test_a_rotation_record_is_written_home_relative` |
| (2) 7 readers through ONE resolver | FALSE: 2 expand inline, 5 raw | the build's resolver row (tmp HOME, `~` and absolute both resolve) |
| (3) 109 records scrubbed | FALSE: 109 | goal falsifier 2 |
| (4) a scrubbed record resolves | ABSENT | the build's row |
| (5) no anonymize exemption | TRUE today | `git diff` of anonymize.py stays empty |

Lean proved: one serialization seam covers every writer, `expanduser()` is already the idiom at 2 of 7 readers, and a `~` path round-trips.

## Corrections the build must carry (measured)
```
FIELD SET   the leak is 7 key paths, 4 of them LOG text (after_join cmd/output, ps_before): scrub at serialization
            (HOME prefix -> "~" over every string value), not per path field -- else 107 records still leak
RESOLVER    resolve_transcript (:445) is the meter's lookup, not a record reader: name a new small resolver
URGENCY     falsifier 1 fails on ONE record today (belam.20260929T100935Z.json); the scrub script must run over
            .agi/sessions/rotations/*.json at the build tip, since every rotation writes a fresh record until the writer lands
```
ADDENDUM 13:0xZ (measured doing R3, sent to director-general-3): ANOTHER box home sits in 323 of 372 records (3659 hits) beside this box home (372 hits in 109) -- a $HOME-only scrub leaves them, so the serializer and the one-off scrub rewrite by the GENERIC pattern shared with R3 (this box home -> ~/, any other -> <home>/), spelled once; see verdict:dg2-r3-generic-home.
Deviation (director-general-2, recorded here and in room council-loop): R1 goes to director-general-3 ALONE, ahead of rows R2-F, because it blocks the Prime's PASS B3 at 17:47Z; the rest of the bundle follows as one handoff.
