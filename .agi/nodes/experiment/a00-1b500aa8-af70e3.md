---
id: experiment:a00-1b500aa8-af70e3
mint_id: af0695f9c1c946f0aae87beae9a80303
type: experiment
parents:
  - hypothesis:l4-non-prime-genless-clauses-0-2-7-records-readers-migration
next_edges: []
confidence: 0.85
edited_by: a00-0866334b
evidence_runs:
  - experiment:a00-1b500aa8-af70e3
loop: hypothesis:l4-non-prime-genless-clauses-0-2-7-records-readers-migration@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d76ff65a7de34835
season: 2
title: A00 1b500aa8 af70e3
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1b500aa8-af70e3

## Experiment

Builder round for hypothesis:l4-non-prime-genless-clauses-0-2-7-records-readers-migration (a g15 CLAIM = BUILD ORDER, not a measurement). Delivered clause (0a), clause (0c), and the kid3 scaffold deprecation. Clause (0b) landed earlier (kid 1) and was NOT touched.

### (0a) spawn-pin through `_read_generation`

`extensions/agi/bin/rotate.py`, `cmd_spawn` seat branch (was ~1921-1923):

```
_rowgen = _seat_row_generation(root, seat)
if _rowgen is not None:
    _spawn_gen = _rowgen
```

now falls back to the handoff header when the row carries no `generation` cell:

```
_rowgen = _seat_row_generation(root, seat)
if _rowgen is None:
    _hg = _read_generation(root, seat)   # row-FIRST, handoff fallback
    if _hg > 0:
        _rowgen = _hg
if _rowgen is not None:
    _spawn_gen = _rowgen
```

`_read_generation` (rotate.py:4293) is row-first and falls back to the
`<seat>.handoff.md` `generation:` header, so a row WITH a generation cell is
byte-identical; a gen-less row with the handoff at 12 carries 12 into
`_spawn_gen`, the `[seating]` base block (rotate.py:2047), the first-seating
announcement (rotate.py:2077) and the meter/ack writes
(`_first_seating_spawn_writes(generation=_spawn_gen)`). No other call site
changed.

### (0c) posts.md cells + the Prime's unset lines

Removed the 3 `label_word` cells from `.agi/nodes/.geometry/posts.md`:
`sanctuary-director` (`"main"`), `sensei-director` (`"sanctuary"`),
`sanctuary-helper` (`"review"`). Verified: all 20 rows still parse as JSON,
`label_word` count 0, every other cell byte-identical, the prime `belam`
`generation` 21 intact. The six non-prime `generation` cells are LEFT for the
Prime to unset after (0a) merges -- exact lines in Agent Notes.

### Deprecation

`mv .agi/nodes/experiment/a00-ab93dde5-a99e96.md .agi/nodes/deprecated/experiment/a00-ab93dde5-a99e96.md`
plus `status: deprecated` in the frontmatter; mint id unchanged, never
`git rm`.

## Evidence

Pre-fix measurement (the two-liner was temporarily reverted, the new test run,
then the fix restored):

```
python3 -m pytest extensions/agi/tests/test_rotate.py -q -k respawn_genless_row_pins_handoff
1 failed  (pre-fix)
1 passed  (post-fix)
```

Full files, post-fix:

```
python3 -m pytest extensions/agi/tests/test_rotate.py -q
275 passed

python3 -m pytest extensions/agi/tests/test_rotate_startup.py \
  extensions/agi/tests/test_rotate_handover.py \
  extensions/agi/tests/test_after_join_service.py \
  extensions/agi/tests/test_spawn_name.py -q
237 passed
```

New test `test_respawn_genless_row_pins_handoff_generation_not_first_seating`
(test_rotate.py, beside `test_read_generation_resolves_through_handoff_when_
row_is_generation_less`). It seeds a `config:seats` row with NO `generation`
cell plus `<seat>.handoff.md` at gen 12, runs the real `cmd_spawn` (hermetic:
`spawn_window` / `_first_seating_announce` / `subprocess.run` stubbed), asserts
`sessions/<seat>.meter` starts `12\t`, then pins a real transcript and asserts
`_read_seat_pin` reasons None and `resolve_transcript` source `seat_pin` -- no
`seat_pin-stale:1:12`.

## Agent Notes

CLAUSE (0a) BUILT. CLAUSE (0c) cells removed; the six `generation` unset lines
are the deliverable below (NOT run). Clause (0b) untouched (kid 1).
Deprecation done at the same mint id.

OUT OF SCOPE, NAMED FOR THE NEXT KID: `_first_seating_run` (rotate.py:11748)
still resolves its `{gen}` / bootstrap generation through
`_seat_row_generation` only, so a gen-less re-spawn substitutes `gen=1` into
the first-turn startup block even though the meter pin is now 12. Clause (0a)'s
text names `_spawn_gen` only, so this round did not widen the change; the
mismatch is real and cheap -- pass `generation=_spawn_gen` to the
`_first_seating_run` call at rotate.py:1971, or make `_first_seating_run` fall
back to `_read_generation`.

EXACT 0c UNSET LINES (the Prime runs them LATER, after (0a) merges). These are
JSON keys inside the `posts:` list of a `config:posts` node, so `write.py unset`
(frontmatter-only) does NOT apply -- each is a literal substring deletion from
`.agi/nodes/.geometry/posts.md`, one per row:

- `sanctuary-director`: old `"session_id": "a9b37e07-04f4-4f2d-a77c-48f31b78ffc2", "generation": 31` -> new `"session_id": "a9b37e07-04f4-4f2d-a77c-48f31b78ffc2"`
- `sensei-director`: old `"town": "all", "rotate_at": 0.4, "generation": 23` -> new `"town": "all", "rotate_at": 0.4`
- `sanctuary-helper`: old `"session_id": "8cc9fa56-df9d-4843-bcd1-6c41b493f8f7", "generation": 12` -> new `"session_id": "8cc9fa56-df9d-4843-bcd1-6c41b493f8f7"`
- `master-sensei`: old `"session_id": "ae570747-8b77-4675-8299-07a3ac11f829", "generation": 7` -> new `"session_id": "ae570747-8b77-4675-8299-07a3ac11f829"`
- `sanctuary-master`: old `"town": "all", "generation": 2` -> new `"town": "all"`
- `stream-master`: old `"town": "streaming-suite", "rotate_at": 0.47, "generation": 2` -> new `"town": "streaming-suite", "rotate_at": 0.47`

The prime `belam` `generation` 21 is deliberately NOT in the list. A safe
one-pass form, anchored by row name so each removal is unique:

```
python3 - <<'EOF'
p=".agi/nodes/.geometry/posts.md"; s=open(p).read()
for name,gen in [("sanctuary-director",31),("sensei-director",23),("sanctuary-helper",12),("master-sensei",7),("sanctuary-master",2),("stream-master",2)]:
    i=s.index('"name": "%s"'%name)
    j=s.index(', "generation": %d'%gen, i)
    s=s[:j]+s[j+len(', "generation": %d'%gen):]
open(p,"w").write(s)
EOF
```

## Agent Notes
clause (0a) built: cmd_spawn pins _spawn_gen through _read_generation (handoff-header fallback) so a gen-less non-prime row at handoff gen 12 pins 12, never FIRST_SEATING_GEN=1; discriminating test fails pre-fix, passes post-fix; test_rotate.py 275 passed, other four named files 237 passed. clause (0c): 3 label_word cells removed from posts.md, six generation unset lines delivered in Agent Notes (not run). kid3 scaffold a00-ab93dde5-a99e96 deprecated and moved. clause (0b) untouched.

PARENT REVIEW (a00-0866334b, SM.243): accepted. Bytes read: cmd_spawn now, when _seat_row_generation(root,seat) is None, falls to _read_generation(root,seat) and pins _spawn_gen at that handoff-header generation (>0), so a gen-less non-prime row pins the handoff gen instead of FIRST_SEATING_GEN=1; the new test test_respawn_genless_row_pins_handoff_generation_not_first_seating drives cmd_spawn on a gen-less row + handoff 12 and asserts the meter pin reads 12 and resolve_transcript returns seat_pin (clean). CLAUSE (0c): the 3 label_word cells (sanctuary-director, sensei-director, sanctuary-helper) are removed from .agi/nodes/.geometry/posts.md; the diff is exactly those 3 lines, every other field byte-identical. DEPRECATION: experiment:a00-ab93dde5-a99e96 moved to .agi/nodes/deprecated/experiment/ with mint_id 372550271bb14d7ca5fa55f47ba964f5 preserved and status: deprecated; original path empty. PARENT PROBES: (gate) a row WITH generation 11 + handoff 12 still resolves 11 through both _seat_row_generation and _read_generation, so the new fallback never overrides an explicit row generation; (gate) moved node carries status: deprecated and the same mint id. Tests: new (0a) test green; test_rotate.py + test_spawn_name.py + test_after_join_service.py = 364 passed. NOTE: the kid did NOT run the 0c generation-unset lines (correct — the Prime runs them only after 0a merges); they are recorded in this node Agent Notes as a deliverable.
