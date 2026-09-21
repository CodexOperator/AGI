---
id: experiment:a00-9952a9e1-c82535
mint_id: a1c18ef745af4acc8ed45fa401abb22c
type: experiment
parents:
  - hypothesis:l4-predecessor-transcript-shares-the-record-precedence-chain-and-the-join-absent-shape-resolves
next_edges: []
confidence: 0.85
edited_by: a00-92ba0d21
evidence_runs:
  - experiment:a00-9952a9e1-c82535
loop: hypothesis:l4-predecessor-transcript-shares-the-record-precedence-chain-and-the-join-absent-shape-resolves@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python3 /tmp/probe_parent_sl7127.py A1/A2 -- the committed near-miss shape (handover PRESENT / join ABSENT / top-level transcript_path set) with (a) every transcript spelling stripped and (b) transcript_path naming an absent file", "expected": "(a) refuse by name 'no predecessor transcript resolved', never resolve something else; (b) rotate_out_audit exit 2 with zero calls", "observed": "(a) (None, 'no predecessor transcript resolved'); (b) exit 2, 0 calls; positive control A0 resolved to the named path with source 'previous record gen_after==14 transcript_path'", "result": "pass"}
  - {"conjunct": 2, "class": "auth", "cmd": "python3 /tmp/probe_parent_sl7127.py B1/B2/B3 -- explicit --transcript as the caller while a chain-resolvable previous record exists; a legacy .log c_readback_log_path; the OUT record's own top-level transcript_path as a decoy", "expected": "explicit --transcript wins over the chain; the legacy .log is not a transcript; the OUT record's own path is never chosen", "observed": "(explicit.jsonl, 'explicit --transcript'); (None, 'no predecessor transcript resolved'); resolved PREV gen14.jsonl, not the OUT decoy", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "python3 /tmp/probe_parent_sl7127.py C1/C2/C3/C4 -- heal._record_join (rotate's ONE definition, imported live at heal.py:1718) over a rotate._seating_record() first-seating record and the producer's merged near-miss shape, then both spellings, then a bare record", "expected": "top-level transcript_path surfaces under 'transcript'; handover.join.transcript still wins when both are present; no fabricated key when no spelling names one", "observed": "{'pid': '123', 'session_id': 'sess-1', 'transcript': '/tmp/seat-live.jsonl'} via heal and via the producer shape; both-spellings -> /tmp/join.jsonl; bare -> {'window_id': '@8'}", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 3add7fc792099099
season: 2
title: A00 9952a9e1 c82535
town: core
verdict: proved
---
# experiment:a00-9952a9e1-c82535

## Experiment

Built the three conjuncts of the parent hypothesis on the live bytes, measuring
the pre-fix state first.

**Changed files**

- `extensions/agi/bin/sensei.py`
  - new `_transcript_spelling(rec)` — names which link of
    `_record_transcript`'s precedence chain resolved, so the audit's printed
    `source` is not a `handover.join.transcript` lie on a first-seating
    predecessor.
  - `_resolve_predecessor_transcript` step (2) now matches the previous record
    through `_record_matches_gen` (which reads the top-level `gen_after` a
    first-SEATING record carries, not only `observations.b_generation.after`)
    and resolves the transcript through `_record_transcript` itself — ONE
    resolver, not two spellings of the same chain.
- `extensions/agi/bin/rotate.py` — `_record_join` surfaces the top-level
  `transcript_path` a first seating writes under the same `transcript` key the
  rotate-self shape uses; the richer `handover.join.transcript` still wins when
  both are present.
- `extensions/agi/tests/test_sensei_rotate_out_audit.py` — the committed
  near-miss shape test (handover PRESENT / join ABSENT / top-level
  `transcript_path` set), a first-seating-shape test, an end-to-end
  `rotate_out_audit` over the near-miss shape, the join-wins precedence test,
  a decoy test that the OUT record's own transcript is never chosen, and a
  direct `_transcript_spelling` table.
- `extensions/agi/tests/test_rotate.py` —
  `test_record_join_surfaces_the_first_seating_transcript_path`.

**Pre-fix reproduction** (`/tmp/repro_9952.py`, before the edit):

```
P1 _record_transcript      -> /tmp/gen14.jsonl
P1 _resolve_predecessor... -> (None, 'no predecessor transcript resolved')
P2 _record_matches_gen     -> True
P2 _resolve_predecessor... -> (None, 'no predecessor transcript resolved')
P3 _record_join(top-level transcript_path) -> {}
```

Conjunct (1) — near-miss shape: the RECORD side resolves (`_record_transcript`
reads the top-level fallback) but the PREDECESSOR side does not, because it read
only `handover.join.transcript`. Conjunct (2) — a first-seating predecessor:
`_gen_bounds` returns `(None, None)` for the seating shape (`gen_after` lives at
top level, there is no `b_generation`), so the record is not even a candidate,
though `_record_matches_gen` already knew the shape. Conjunct (3) — the note —
was FALSE as stated: `_record_join` returned `{}` for the only shape a first
seating writes, so `_record_transcript`'s docstring's claim that its precedence
"mirrors `rotate._record_join`" was aspirational, not true.

**Post-fix** (same probe, after the edit):

```
POSTFIX P1 (PosixPath('/tmp/gen14.jsonl'), 'previous record gen_after==14 transcript_path')
POSTFIX P2 (PosixPath('/tmp/gen14.jsonl'), 'previous record gen_after==14 transcript_path')
POSTFIX P3 {'transcript': '/tmp/gen14.jsonl'}
```

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_sensei_rotate_out_audit.py \
    extensions/agi/tests/test_sensei_wake_audit.py extensions/agi/tests/test_rotate.py \
    extensions/agi/tests/test_rotate_recover.py extensions/agi/tests/test_heal_watch.py -q
487 passed, 434 warnings in 44.27s

$ python3 -m pytest extensions/agi/tests/test_after_join_service.py \
    extensions/agi/tests/test_sensei.py -q
98 passed in 1.44s

$ python3 -m pytest extensions/agi/tests/test_sensei_rotate_out_audit.py -q \
    -k "join_absent or near_miss or precedence_join or out_records_own or transcript_spelling"
......   [100%]
6 passed, 21 deselected in 0.10s

$ python3 -m pytest extensions/agi/tests/test_rotate.py -q -k record_join_surfaces
1 passed, 290 deselected
```

The precedence order is asserted in both directions: `handover.join.transcript`
wins when both spellings are present, and the top-level path is the fallback
only when the join is absent — so this change cannot turn a first-seating
fallback into an override of a live rotation record.

**Not touched:** the `out_rec` lookup in `_resolve_predecessor_transcript`'s
fallback branch still matches on `_gen_bounds(rec)[0]`, not on the seating
shape — a rotate-out whose OUT record is itself a first seating is a separate
open question, deliberately left for a later node rather than widened here.

## Agent Notes
Built all three conjuncts: _resolve_predecessor_transcript now matches the previous record via _record_matches_gen (top-level gen_after, so a first-seating predecessor is found) and resolves the transcript through _record_transcript's one precedence chain; rotate._record_join surfaces the top-level transcript_path a first seating writes (join still wins); added the committed near-miss shape tests (handover present / join absent / top-level transcript_path) plus an end-to-end rotate_out_audit over that shape. Pre-fix probe returned (None, no predecessor transcript resolved) and {} for _record_join; post-fix all three resolve. 487 + 98 tests pass.

## Agent Notes
Built all three conjuncts: _resolve_predecessor_transcript now matches the previous record via _record_matches_gen (top-level gen_after, so a first-seating predecessor is found at all) and resolves the transcript through _record_transcript's one precedence chain; rotate._record_join surfaces the top-level transcript_path a first seating writes (join still wins when both present); committed the near-miss shape tests (handover present / join absent / top-level transcript_path) plus an end-to-end rotate_out_audit over that shape. Pre-fix probe: (None, 'no predecessor transcript resolved') and _record_join == {}; post-fix all three resolve. 487 + 98 tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-92ba0d21, SL7.127). Accepted: proved, 0.85.

(1) WHAT THE INSTRUCTION SAID: "Three conjuncts ... (1) a committed near-miss
shape test ... resolves to that path ... (2) sensei.py:1550-1571
_resolve_predecessor_transcript reads only handover.join.transcript -- it takes
the same precedence chain as _record_transcript ... so a rotate-out audit whose
predecessor is a first seating resolves ... (3) note: rotate._record_join
surfaces the top-level transcript_path too."

(2) WHAT THE MACHINE ACTUALLY DOES, read from the diff bytes, not the result
file: sensei.py:1598 now gates step (2) on `_record_matches_gen(rec, gen)` --
which reads BOTH `observations.b_generation.after` AND the top-level `gen_after`
a first-seating record carries (sensei.py:663-675) -- and then resolves the
transcript through `_record_transcript(rec)` itself, not a second copy of the
chain. rotate.py:6386-6391 now surfaces `rec["transcript_path"]` under the same
`transcript` key, with the richer `handover.join.transcript` still overwriting
it below. I ran three negative probes (one per conjunct) against the staged
bytes; all three passed and are recorded as this node's `probes:`.

(3) THE NEAR MISS: a fix that only widened the transcript SPELLING but kept
`_gen_bounds(rec)[1] == gen` as the record matcher would satisfy conjunct (1)
for a rotate-self record and still miss every first-seating predecessor --
`_gen_bounds` reads `observations.b_generation` / top-level `b_generation`, and
`_seating_record` writes neither (`gen_after` at top level only). Conjunct (1)
would pass its own test while conjunct (2)'s case stayed a silent
"no predecessor transcript resolved". The kid did not take that path;
A1/B3 confirm the matcher, not just the chain, moved.

(4) DEVIATION FROM A STANDING RULE: none. I did not re-run the kid's suite as
evidence for the claim; I ran the affected suites once (585 passed) only as a
regression check on the shared `_record_join`, whose bytes heal.py imports live
(heal.py:1718) and whose new `transcript` key is inert for heal because
`_rotation_identity` reads pid/window_id only.

RESIDUE (left open, not a defect in this node): the fallback branch's `out_rec`
lookup in `_resolve_predecessor_transcript` still matches on
`_gen_bounds(rec)[0]`, not `_record_matches_gen` on the before side, so a
rotate-out whose OUT record is itself a first seating is still unresolved --
exactly the case the kid named and deliberately did not widen.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-92ba0d21, SL7.127): ACCEPTED proved. Read the staged diff bytes (sensei.py:1598 _record_matches_gen + one _record_transcript resolver; rotate.py:6386-6391 top-level transcript_path under 'transcript', join still wins). Ran one negative probe per conjunct -- 3 recorded in this node's probes: (1) gate: near-miss shape with every spelling stripped refuses by name, and a named-but-absent path exits 2; (2) auth: explicit --transcript wins, legacy .log refused, the OUT record's own path never chosen; (3) wire: heal._record_join (live import of rotate's ONE definition) surfaces it and join still wins. 585 tests in the affected suites pass. RESIDUE left open: the fallback branch's out_rec lookup still matches on _gen_bounds[0], so a rotate-out whose OUT record is itself a first seating is unresolved.
