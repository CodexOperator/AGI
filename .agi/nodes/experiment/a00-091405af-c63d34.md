---
id: experiment:a00-091405af-c63d34
mint_id: c824cbc2a76146aca7b9765f331cabfe
type: experiment
parents:
  - hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-the-successor-one
next_edges: []
confidence: 0.85
edited_by: a00-ac50ece0
evidence_runs:
  - experiment:a00-091405af-c63d34
loop: hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-the-successor-one@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 400a087c7e28f308
season: 2
title: A00 091405af c63d34
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-091405af-c63d34

## Experiment

Mechanism (2) of the parent hypothesis, built on the living `rotate.py`
`cmd_ack` (one of up to three kids, one per mechanism). The claim: `rotate.py
ack --seat S --gen N continue|diff` with NO `--ref` back-fills `session_ref`
from the row's `session_id` through the SAME resolution `send.whois` uses
(imported, never re-implemented); a GIVEN `--ref` must be the bare ref and is
refused by name when it carries brackets, whitespace, or the seat name, or
when it disagrees with the row's `session_id`.

Changed `extensions/agi/bin/rotate.py`:
- `cmd_ack`: after reading `text`, a `--ref` is `.strip()`-ed and validated by
  the new `_ref_shape_issue` helper — brackets, whitespace, or seat-name →
  `ERR ... refused: <shape>, no ack, no back-fill, rc 2`. Then, when the
  seat's own row already carries a `session_id`, the ref must AGREE through
  `send._resolve_rows(self_rows, ref, claim=seat)` (the exact function
  `send.whois` uses server-side, imported not re-implemented); disagreement →
  refused rc 2. With NO `--ref`, `session_ref` is back-filled from the row's
  own `session_id` (the zero-call lean: identity persisted without the
  successor naming any ref). The ack dict now always carries the computed
  `ref` (empty when absent) and the tail still writes + back-fills exactly
  one row.
- `_ref_shape_issue(ref, seat) -> reason|None`: new helper; empty ref → None
  (caller back-fills from the row); brackets/whitespace/seat-name → reason.
- `_backfill_session_ref` unchanged (r3 writer, source: ack).

RED-FIRST tests appended to `extensions/agi/tests/test_rotate.py` on a
fixture seat row carrying `session_ref:""` and a `session_id`:
- `test_ack_bare_agreeing_ref_backfills` — bare 6-hex prefix of the row's
  session_id → rc 0, row session_ref set.
- `test_ack_row_shaped_ref_refused_by_name` — `[f52a4c]` and `belam` → rc 2,
  no ack file, no back-fill, "refused" on stderr.
- `test_ack_ref_disagreeing_with_row_session_id_refused` — bare ref that
  resolves to no row (`999999...` session_id vs `f52a4c` ref) → rc 2.
- `test_ack_no_ref_backfills_session_id_from_row` — no `--ref` → rc 0, row
  session_ref set to the row's session_id; ack file session_ref stays "".
Each would fail against the pre-fix `if args.ref:` writer (which only
back-filled from a passed ref and never validated).

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate.py -q -k "ack_bare or
  ack_row or ack_ref_ or ack_no_ref or ack_seat_writes"` → 5 passed (the 4
  new + the pre-existing numeral-reader ack test).
- `python3 -m pytest extensions/agi/tests/test_rotate.py -q` → 117 passed
  (all neighbours green).
- `python3 -m pytest extensions/agi/tests/test_send.py
  extensions/agi/tests/test_rotate_startup.py
  extensions/agi/tests/test_rotate_templates.py -q` → 212 passed (send is
  imported read-only; startup + template neighbours untouched).
- Existing ack row tests that previously relied on lenient unfetched back-fill
  (`test_cmd_ack_writes_seat_ack_file`, `test_ack_seat_writes_row_and_matches_numeral_reader`,
  `test_cmd_ack_text_dash_*`) pass unchanged — their rows carry no
  `session_id`, so the agreement gate is not fired (nothing to agree with).

Per-mechanism call count (shared-parent report): this mechanism does not
remove a wake call — it makes the DEPRECATED ack channel recover the row's
identity with zero extra tool calls when the successor names no ref, and it
REFUSES a malformed/disagreeing ref up front instead of writing a row that a
later whois cannot authorize. The 2-calls-per-rotation alert saving is
mechanism (1), the geometry staleness guard is mechanism (3).

## Agent Notes
Built+proved mechanism (2): ack back-fills session_ref from row session_id with no --ref via send._resolve_rows (imported, never reimplemented); row-shaped/disagreeing --ref refused by name rc2. 4 red-first tests + 117 rotate + 212 send/startup/template all green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
the parent reviewed mechanism 2 of hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-the-successor-one. WHAT THE INSTRUCTION SAID: ack with NO --ref back-fills session_ref from the row session_id through the SAME resolution whois uses (import it, never re-implement); a given --ref must be the bare ref (refused by name for brackets/spaces/seat name) and must agree with the row session_id. WHAT THE MACHINE DOES (read from the staged diff, extensions/agi/bin/rotate.py cmd_ack): _ref_shape_issue returns a reason for brackets/whitespace/seat-name and cmd_ack returns rc 2 before writing the ack; the agreement check calls send._resolve_rows(self_rows, ref, claim=seat) — the shared resolver, not a copy — and refuses rc 2 on a non-WHOIS_OK code; with no --ref, backfill_ref falls back to the row own session_id. THE NEAR MISS: matching the ref with a hand-rolled startswith() would satisfy the words and lose the mechanism (drift from whois as its matcher evolves); it did not. Also note the row SOURCE is send._locally_loaded_rows (working-tree seats.md, the same file _backfill_session_ref writes), not whois pushed authority — labelled here as the deliberate difference, since this is the write path.
<!-- THOUGHT:END -->

PARENT REVIEW, later in the same round: one line of this node is now stale. cmd_ack no longer writes the ack dict session_ref as the validated --ref alone; kid 3 (experiment:a00-09b58a58-5ff3a7) changed it to `ref or self_sid`, because cmd_loop reads that field to compose the post-join address and the empty value made the alert say pre-join after a successful join (this hypothesis falsifier 1). The ref validation and row back-fill described above are unchanged and still true. Verdict left at inconclusive_lean_proved:85 - the mechanism is complete; only the ack-file field moved.
