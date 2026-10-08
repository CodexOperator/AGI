---
id: experiment:a00-881fe4f0-2312e1
mint_id: 3d8a6f287c9a4219bae361c70db195b6
type: experiment
parents:
  - hypothesis:l4-a-post-row-carries-a-session-name-cell-the-registry-join-resolves-and-session-ref-is-never-the-session-uuid
next_edges: []
confidence: 0.8
edited_by: a00-f149ffed
evidence_runs:
  - experiment:a00-881fe4f0-2312e1
loop: hypothesis:l4-a-post-row-carries-a-session-name-cell-the-registry-join-resolves-and-session-ref-is-never-the-session-uuid@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7c6f24836face138
season: 2
title: fix-16-session-name-self-row-fixture-regressions
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-881fe4f0-2312e1

## Experiment

Re-brief round closing the regression kid 1 (a00-5ddf1181-b5edec) left open. The
`session_name` cell was added to the live self-row schema and to the row writers
(`_successor_row_write`, `_backfill_session_ref`), but kid 1 ran only a filtered
subset (`-k test` on 3 files) and reported green, missing 16 full-suite failures
all of one mechanism:

`write.EditError: config nodes (config:seats): ... field 'session_name' is not in
the self-row fields [...] declared by the node's schema`

Kid 1 ALWAYS emits `session_name` (even `''`) as the claim's testable sentence
requires; the data-driven write guard (L4.110) then refuses the write WHOLE when
the fixture's hardcoded `self_row` does not declare `session_name`. The fixtures
were a stale duplicate of the live schema — pre-`session_name`.

## FIX TAKEN: Option (A)

Kept the literal `''` write (kid 1's `_successor_row_write`/`_backfill_session_ref`
always emit the cell, even empty) and brought every stale hardcoded `self_row`
fixture up to the live schema. Mechanism reason: the claim's testable_claim
literally states the cell is written `''` when the join did not resolve; the cell
is documented and admitted by the live schema (`[config].md` lists `session_name`).
The 16 failures were NOT behavior bugs — they were test asserts of a write the
guard correctly refused against a stale field list. Fixing production to dodge a
stale fixture (option B, omitting the cell on a miss) would contradict the claim's
`''` sentence and would not address the recurring fixture-drift class.

All 7 stale `self_row` sites updated (not just the 3 failing files), matching the
live schema field order (`session_ref, session_name, session_id, ...`):
- `test_rotate_handover.py` :406, :655, :843 — +`session_name`
- `test_rotate_identity_main.py` :39 — +`session_name`
- `test_heal_ack_rotation.py` :68 — +`session_name`
- `test_post_rename.py` :230 — +`session_name` (unused-fallback but kept in sync)
- `test_write_self_row.py` :31 — `SELF_ROW_SCHEMA` fallback +`session_name`

One further test-only change, forced by the feature itself: in
`test_ack_rotate_self_shaped_row_stays_byte_identical` the assertion
`"back-filled session_ref=r1 into own row" in out` rotted — the join's `name`
(which falls back to the seat name) is now written and printed, so the line reads
`back-filled session_ref=r1, session_name=adv-s into own row (source: ack), joined
by @77`. Relaxed to `"back-filled session_ref=r1" in out` (the ref back-fill still
reported) while keeping `"pid=" not in out` and `"session_id=" not in out` — same
stale-with-feature class as the fixtures. No production code was changed.

## Evidence

Targeted re-run (self_row-bearing + feature files):
`test_rotate_handover.py test_rotate_identity_main.py test_heal_ack_rotation.py
test_write_self_row.py test_post_rename.py test_rotate_startup.py test_rotate.py`
→ **445 passed**.

FULL suite (all 167 test files, `extensions/agi/tests/test_*.py
extensions/agi/tests/*/test_*.py`) →
**`1 failed, 4231 passed, 14 skipped, 1 xfailed`** (438.08 s).

Scope identical to the parent's baseline (4247 collected both); the only change
vs `17 failed, 4215 passed` is the 16 regression tests now passing (+16 passed,
-16 failed).

The one remaining failure is **pre-existing and NOT-this-round**:
`test_seat_alias_notice.py::test_static_scan_reports_site_count_and_names`
(`assert 22 == 21` — argparse `--seat` site count drifted; kid 1 touched no
argparse site). Left unfixed per brief.

## Agent Notes
Locked loop SL7.96. Verdict proved by measurement: full-suite green for all 16
regressions, only the named pre-existing seat-alias failure remains. Mechanism
reason for option (A) documented in body.

## Agent Notes
Option A: kept literal '' session_name write, synced all 7 stale self_row fixtures to live schema; relaxed one rotted byte_identical substring assert. Full suite 1 failed/4231 passed/14 skip/1 xfail (all 16 regressions green; only pre-existing seat-alias 22==21 remains, not-this-round).

Full-suite re-run after Option A: 1 failed / 4231 passed / 14 skipped / 1 xfailed; parent reproduced the five fixture files (94 passed) and the feature files (664 passed + the one pre-existing failure).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review kept proved. Reproduced independently: all 7 stale self_row fixture sites now list session_name (grep), test_rotate_handover + test_rotate_identity_main + test_heal_ack_rotation + test_write_self_row + test_post_rename = 94 passed, and test_rotate + test_send + test_rotate_startup + test_seat_alias_notice = 664 passed with exactly one failure (the pre-existing seat-alias 22==21 count). The option-(A) mechanism reason is the one this parent would give: the 16 red tests were not behaviour bugs, they were fixtures asserting against a write the L4.110 data gate correctly refused, and the fixture was a stale duplicate of the live schema — fixing production to dodge a stale fixture would have contradicted the claim's own literal ''' write. Caveat the parent cannot close: the seat-alias failure is reasoned not-this-round (neither kid touched an argparse --seat site; the file mtimes are base) but it was NOT measured on a pristine base — a reader who needs that must measure it.
<!-- THOUGHT:END -->
