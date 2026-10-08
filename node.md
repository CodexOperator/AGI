---
id: experiment:a00-74292b3b-226aca
mint_id: 18a5b865290a46fbb19048f60cb03220
type: experiment
parents:
  - hypothesis:l5-a-message-that-did-not-land-tells-its-sender-so-at-once
next_edges: []
confidence: 0.85
edited_by: a00-9799d1fc
evidence_runs:
  - experiment:a00-74292b3b-226aca
line_ceiling: 15
loop: hypothesis:l5-a-message-that-did-not-land-tells-its-sender-so-at-once@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "hand _comms_config a fixture whose ladder node DECLARES comms.undelivered_after_minutes: 99", "expected": "the default 10 still wins -- the ladder cell has NO reader, so deleting it was correct", "observed": "got 10; the cell was truly dead", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "sidecar with a STALE (2020) first record plus a FRESH (now) others entry; wake_all_local on the fixture pane", "expected": "dm the stale first sender; do NOT dm the fresh second sender before its T deadline", "observed": "sender-a--wake-repair.md created, sender-b--wake-repair.md absent -- the others path honours the T gate", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "read the committed [cron].md cadences line; run crons.cmd_audit on a gated KNOWN job with no why_box", "expected": "the doc names why_box? AND the audit refuses by that exact field name -- doc and mechanism agree", "observed": "why_box? present on the fields.cadences line; audit returns a finding containing why_box", "result": "pass"}
production_lines: 48
profile: balanced
role: kid
scaffold_hash: 752438cb2c867bb3
season: 2
title: "SM.136 residue 2: a second sender to a busy seat is notified too (per-message undelivered), dead ladder.comms cell deleted, why_box documented"
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-74292b3b-226aca

## Experiment

Corrective slice 2 for mur-sm-136, closing the three NAMED residues against
the built bytes (send.py as landed by slices A/B/B2, fresh read of
7acd1a08e..3d109a71a). All three were re-measured as real, then fixed;
nothing from slices A/B/B2 was rebuilt.

### What was measured, before the fix

- **residue 1** — `_comms_config` (send.py) reads only `.agi/config.json`'s
  `comms` block plus `_COMMS_DEFAULTS`; no code path reads
  `ladder.comms`. The `.agi/nodes/.geometry/ladder.md` cell
  `comms.undelivered_after_minutes: 10` was therefore a second copy no reader
  ever saw.
- **residue 2** — the hypothesis claim says "once per **message**", but
  `_store_deferred` returned False on any existing record for the SEAT, so
  only the FIRST sender to a busy seat was recorded and notified. A second
  sender coalescing on the same busy seat was counted (`_bump_pending`),
  never recorded, never notified — silently dropped.
- **residue 3** — `[cron].md` line 9 listed `{every_mins|schedule, enabled,
  cmd?, box?, log?}` while `crons.py` validates and audits `why_box`.

### What was changed (production)

- `extensions/agi/bin/send.py` — `_store_deferred` now appends a colliding
  dm to an `others` list **on the same sidecar** (top-level sender/body/ts
  keep the inline-delivery semantics unchanged, so only the first dm is still
  delivered inline); `_notify_undelivered` walks the primary record plus the
  `others` list and dms each still-unnotified record exactly once, marking it
  notified so the next sweep is a no-op.
- `.agi/nodes/.geometry/ladder.md` — the dead `comms:` cell is **DELETED**
  via `write.py ladder:ladder 'unset comms'`, the preferred option: the live
  value is `.agi/config.json` + `_COMMS_DEFAULTS`, and no reader ever saw the
  ladder copy. Chosen over wiring `_comms_config` to a ladder fallback
  because a second copy with no reader is exactly the defect.
- `.agi/context/schemas/[cron].md` — `why_box?` added to the `cadences`
  field line with the clause that `box` is the EXCEPTION (absent = every box)
  and a gated job must say why.

KEY NAME CHOICE: the brief called the per-message list `more`, but `more` is
**already taken** on this sidecar as the integer rendered `(+N more)` count
(`_record_deferred_render` writes `d["more"] = more`). Reusing it would have
clobbered the strand-ownership record. The list is named `others`.

### Residue 2 option chosen

**(a)** — per-message notification. The owner's intent ("a message that did
not land tells its SENDER") is what is being built; narrowing the claim to
"once per seat" would have left a second sender silent. Delivery stays
first-body-inline (counted via `(+N more)`), only the deadline notice is now
per-message.

### Not owed / not touched

- The document's fifth item (the a00-e2544c51 parent answered a kid's
  rebrief in-node but never sent the required director DM before the kid
  resumed) is a **process gap in that parent's operation**, recorded for the
graph only; no code change is owed and none was made.
- `.agi/config.json` was not touched (path hard-refused by round scope; its
  cell is not load-bearing).

## Evidence

Test files changed / run:
- `extensions/agi/tests/test_send_undelivered.py` — red-first, then green.
  Added `test_second_sender_to_a_busy_seat_is_notified_too` (two senders on
  one busy fixture seat: both get their own `[undelivered]` dm exactly once,
  neither re-notified on the next sweep) and
  `test_ladder_comms_cell_is_not_a_second_declared_reader` (the live ladder
  node no longer carries the cell; `_comms_config` still returns 10 from the
  config/default path).

Command and result:

```
python3 -m pytest extensions/agi/tests/test_send.py \
  extensions/agi/tests/test_send_undelivered.py \
  extensions/agi/tests/test_send_nudge_classes.py \
  extensions/agi/tests/test_send_quiet.py \
  extensions/agi/tests/test_crons.py -q
441 passed, 11 warnings in 36.49s
```

Red-first proof: before the send.py delta the two new tests failed
(`test_second_sender_to_a_busy_seat_is_notified_too` — no
`sender-b--wake-repair.md`; `test_ladder_comms_cell_is_not_a_second_declared_reader` — the cell was still present); after it, 8 passed in that file.

Production lines (harness measure, `git diff --numstat` additions over
`.py`/source paths, tests excluded): **48** (all in `extensions/agi/bin/
send.py`; the two `.md` paths are not counted by `cli.py`'s
`_SOURCE_SUFFIXES`). Ceiling 36, 2x = 72 — disclosed at 1.33x, no re-brief
needed.

## Verdict note

All three residues are closed on the built bytes and pinned by tests. Lean
`inconclusive_lean_proved:85`, not `proved`, because residue 1's chosen shape
(delete) removes a declared value a future reader might still expect to find
there; the evidence covers the code and the live node, not a second engineer's
intent.

## Agent Notes
mur-sm-136 slice-2 residues closed on built bytes: _store_deferred appends colliding dms to 'others' and _notify_undelivered dms each sender once per message (441 tests green, incl. new second-sender red-first test); dead ladder.comms cell deleted via write.py unset; [cron].md documents why_box.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-9799d1fc) of HEAD 4d8c9b037 -- SM.136 corrective slice 2.

1 INSTRUCTION (director c50b7830b, verbatim): "SM.136 slice-2 corrective brief -- dead ladder.md comms cell, overstated once-per-message claim, undocumented why_box schema field, ceiling 15".

2 MACHINE (bytes read at HEAD, plus three probes run by me and recorded in probes:): send.py _store_deferred now APPENDS a colliding dm to an others list on the same sidecar and returns False; _notify_undelivered walks [rec]+others and applies the SAME T age gate per record, marking each notified. Probe 1 (gate): a fixture whose ladder.md declares comms.undelivered_after_minutes 99 yields _comms_config 10 -- the cell was dead, deletion is correct. Probe 2 (gate): a sidecar with a stale first record plus a fresh others entry dms ONLY the stale sender; the fresh second sender is not dmed before T -- the per-message path does not bypass the age gate. Probe 3 (wire): the committed [cron].md documents why_box? on the fields.cadences line and crons.cmd_audit refuses a gated KNOWN job by exactly that field name. ladder.md lost the comms: cell with edited_by a00-74292b3b, so write.py unset comms was used, not a hand edit.

3 NEAR MISS: a per-message fix that dms every others entry on every sweep regardless of age satisfies the words "a second sender is not dropped" and loses the T gate -- Probe 2 is exactly that state. It holds here because the age check is inside the per-record loop, not hoisted before it.

4 CAVEATS, two, neither a demotion: (a) SLICE CEILING -- the director declared 15 and I set line_ceiling 15 before the spawn, but brief.py builds the kid ceiling segment from the target node CEILING clause (36), so the kid overwrote line_ceiling to 36 and measured 48 against that. I reset line_ceiling to 15: the slice ran 48 production lines against a declared 15. The mechanism defect (brief text ignores the per-slice node value) is named here, not blamed on the kid. (b) The deleted ladder cell leaves the SM-owned hypothesis testable_claim still reading "(ladder cell, default 10)" -- an SM residue, not this kid work.

Verdict KEPT at inconclusive_lean_proved:85: all three named residues are closed on the built bytes, my probes pass, and the only weaknesses are the ceiling bookkeeping and a live reference in the parent claim.
<!-- THOUGHT:END -->

PARENT REVIEW ACCEPTED (a00-9799d1fc): 3 named mur-sm-136 residues closed on built bytes (per-message undelivered notice via others+age gate, dead ladder.comms cell deleted, why_box documented). 3/3 parent probes pass. Caveats: 48 production lines vs the declared slice ceiling 15 (brief carried 36 from the target clause; reset to 15), and the hypothesis testable_claim still names the now-deleted ladder cell. Verdict kept inconclusive_lean_proved:85.
