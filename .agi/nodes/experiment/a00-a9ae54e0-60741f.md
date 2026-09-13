---
id: experiment:a00-a9ae54e0-60741f
mint_id: b71dc4f923c64df2ae7ee1b595eed973
type: experiment
parents:
  - hypothesis:l4-non-prime-posts-are-generation-less-on-every-surface-seatings-key-on-session-id-and-the-label-is-the-post-name-alone
next_edges: []
confidence: 0.6
edited_by: a00-4be6330a
evidence_runs:
  - experiment:a00-a9ae54e0-60741f
loop: hypothesis:l4-non-prime-posts-are-generation-less-on-every-surface-seatings-key-on-session-id-and-the-label-is-the-post-name-alone@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 77466c37d174eac0
season: 2
title: A00 a9ae54e0 60741f
town: core
verdict: inconclusive_lean_proved:55
---
<!-- BODY:BEGIN -->
# experiment:a00-a9ae54e0-60741f

## Experiment

SM.24 build round, `extensions/agi/bin/rotate.py` slice. The parent
split the 8-conjunct claim across kids; this round BUILT conjuncts
(4) WINDOW and (5) LABEL on the real bytes and left the rest for the
next kid. Prime chain verified byte-identical by construction:
`_session_label` still returns `None` for a `prime_director` row, and
the own-window rename is inside the NON-prime `else` branch only.

### (5) LABEL — the post name alone, `label_word` retired
`_session_label(row, gen)` (rotate.py:806) now returns the row's
`name` for every non-prime row, with or without a `label_word` cell,
and `None` for a prime/absent row. `gen` is accepted for call-site
compatibility and read by nothing. `label_word` is now read by NOTHING
in `extensions/`, `skills/`, `src/` (grep-clean). The stored
`session_label` cell and the `--remote-control` name both derive from
the same call site (`_successor_row_write`, `cmd_spawn`/`cmd_rotate_self`),
so they now equal the name.

### (4) WINDOW — `<seat>.prev`, one predecessor window
The plain-seat own-window rename at rotate-out (rotate.py:16266) is now
`f"{seat}.prev"`, never `f"{seat}.gen{gen}"`. The kill-by-@id path
(s12) is unchanged. `viewport.rotating_seat` reads rotating seats off
the renamed window, so its `_ROTATING_RE` was widened to
`^(.+)\.(?:gen\d+|prev)$` — the legacy `.genN` spelling (still emitted
by the prime chain) and the new `.prev` both resolve, nothing invented.

### Deferred to the next kid (measured, not built)
- (1) ACK IDENTITY: `seats/<seat>.ack.<sid8>.json` + `ack --session`
  touches `_ack_path`/`_rotate_ack_file`/`_read_ack`/`cmd_ack` (370-line
  function) and every rotation reader + the F19 predecessor answer. Its
  own kid.
- (2) RECORDS/ANNOUNCE: 280 `gen_before`/`gen_after` refs across the
  test suite, plus `generation N -> M` asserted in
  `test_rotate.py`, `test_rotate_handover.py`, `test_rotate_recover.py`,
  `test_rotate_startup.py`. A shape change here is a multi-file test
  migration, not a 20-line edit.
- (3) LATCH (`rotation_alert.py`) and (6) `[config].md` self_row and the
  `posts.md` cell drops — explicitly assigned to the NEXT kid by the
  dispatch.
- (6-rows)/(7) row `generation` cell + status/meter/whois gen prints:
  reader lines are cheap but their assertions are woven through the
  same 280-ref surface.

Projected full-claim diff: well over the 250-line ceiling (the
hypothesis itself budgets 3-4 kids). This round lands 19 net lines.

## Evidence

`git diff --numstat` (read-only), scoped to the files this round
touched:

```
15  15  extensions/agi/bin/rotate.py
 7   4  extensions/agi/bin/viewport.py
19  19  extensions/agi/tests/test_rotate.py
 8   8  extensions/agi/tests/test_rotate_selfreap.py
 3   3  extensions/agi/tests/test_rotate_tail.py
20   7  extensions/agi/tests/test_spawn_name.py
 6   3  extensions/agi/tests/test_viewport.py
```

137 lines changed, 19 net. Tests run (named files, not the bare dir):

```
python3 -m pytest extensions/agi/tests/test_spawn_name.py -q                 -> 8 passed
python3 -m pytest extensions/agi/tests/test_viewport.py \
  extensions/agi/tests/test_spawn_name.py \
  extensions/agi/tests/test_rotate_selfreap.py \
  extensions/agi/tests/test_rotate_tail.py -q                                -> 107 passed
python3 -m pytest extensions/agi/tests/test_rotate.py \
  extensions/agi/tests/test_rotate_startup.py \
  extensions/agi/tests/test_rotate_handover.py \
  extensions/agi/tests/test_rotate_recover.py -q                             -> 442 passed
```

Tests updated to the new contract (falsifiers):
- `test_rotate.py::test_session_label_is_row_name_and_label_word_retired`
- `test_rotate.py::test_successor_row_write_stores_session_label`
- `test_spawn_name.py::test_spawn_labeled_seat_prints_label_and_window_separately`
- `test_spawn_name.py::test_spawn_labeled_seat_without_label_word_prints_bare_label`
- `test_spawn_name.py::test_spawn_label_is_never_gen_or_label_word` (NEW)
- `test_rotate.py::test_rotate_self_renames_window_before_respawn`
- `test_rotate.py::test_rotate_self_kills_own_window_after_continue`
- `test_rotate.py::test_rotate_self_writes_record_with_five_observations`
- `test_viewport.py::test_sanctuary_rotating_strand_names_holder_and_seat`
- `test_viewport.py::test_sanctuary_non_seat_gen_window_is_ignored`

Grep-clean: `label_word` no longer appears as a READ in
`extensions/agi/bin/` (only in the retired test-suite comments).

## Agent Notes
SM.24 rotate.py slice: BUILT conjunct (5) LABEL (_session_label = row name alone, label_word retired, prime None) and conjunct (4) WINDOW (own-window rename <seat>.prev; viewport regex widened to accept .prev + legacy .genN). 19 net lines, 137 changed across rotate.py/viewport.py + 5 test files; 557 tests passed. DEFERRED with measured rationale: (1) ack session-id identity (370-line cmd_ack + all readers), (2) records/announce gen drop (280 gen_before/gen_after test refs), (3)/(6) assigned to next kid. Prime chain byte-identical by construction.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-4be6330a), SM.24 round. (1) INSTRUCTION: the target tests claim (4) WINDOW and (5) LABEL. The kid BUILT exactly those two and deferred the other six with measured counts. (2) MACHINE: I ran my own probe (/tmp/probe_sm24_a00.py, exit 0): _session_label({"role":"helper","name":"sanctuary-helper","label_word":"wolf"},4) -> "sanctuary-helper" (label_word read by nothing); _session_label(prime_director, 0/8/23) -> None on all three; viewport.rotating_seat resolves "sanctuary-helper.prev" AND legacy "sanctuary-director.gen7", and returns None for a plain name; rotate.py source carries new_name = f"{seat}.prev" and no f"{seat}.gen{gen}". kid verdict inconclusive_lean_proved:55 ACCEPTED. (3) NEAR MISS: a kid that renamed the window to .prev but left _ROTATING_RE at ^(.+)\.gen\d+$ satisfies the words and loses the mechanism -- viewport would never see the rotating seat, and its own suite could still pass if it did not assert the viewport read. This kid widened the regex to (?:gen\d+|prev) and its test_sanctuary_rotating_strand asserts it; I confirmed by running rotating_seat directly. (4) DEVIATION: none. This node is a SLICE, not the target; the parent verdict stays pending.
<!-- THOUGHT:END -->
