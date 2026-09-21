---
id: experiment:a00-878597a9-c4417b
mint_id: 81f10e00fe8b41a8ac7965c26b19b26c
type: experiment
parents:
  - hypothesis:l4-non-prime-genless-clauses-0-2-7-records-readers-migration
next_edges: []
confidence: 0.85
edited_by: a00-0866334b
evidence_runs:
  - experiment:a00-878597a9-c4417b
loop: hypothesis:l4-non-prime-genless-clauses-0-2-7-records-readers-migration@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c34eb61eb56eb977
season: 2
title: A00 878597a9 c4417b
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-878597a9-c4417b

## Experiment

CLAUSE (0b) of `hypothesis:l4-non-prime-genless-clauses-0-2-7-records-readers-migration`
(the rotate-out-rename-uniqueness half of clause (0); the direction of the other
clauses is untouched and left to their own kids). Two things were built, because
the clause names two halves:

1. **Unique `<seat>.prev`.** `_rename_own_window` (rotate.py:5837) now resolves
   any window ALREADY bearing `new_name` (a previous rotation whose renamed own
   window was never reaped), kills it by its captured `@id` (`_kill_window`),
   and only then renames the plain seat window. `new_name` therefore names
   exactly ONE window afterwards, so a reader that resolves it by name —
   `pred_alive` (`pred_name in pred_raw["names"]`, rotate.py:17445) and the s12
   kill — can never address the stale one.
2. **Own `@id` captured AT the rename.** `_rename_own_window` RETURNS the own
   window's `@id`, resolved from the PLAIN seat name BEFORE the rename (a tmux
   rename preserves the `@id`). `cmd_rotate_self` threads it into
   `handover["own_window"]["id"]` (rotate.py:17150), instead of the old
   post-rename `_successor_window_id(pred_name)` — which is first-match-by-name
   and, with a stale `.prev` present, resolved the STALE window's `@id`.

Supporting seam fix: `_replace_window_name` (rotate.py:5880) now rewrites an
`@<id> <old>` line as `@<id> <new>`, matching real tmux (a rename preserves the
`@id`); the seam previously left `@<id> <old>` untouched, so an @id-bearing own
window kept the seat name.

Test migration (per the round brief, never reverting the code):
`test_rotate_g1517.py::test_spawn_first_seating_role_from_row_and_pin_at_row_gen`
was FAILING 1/6 asserting the RETIRED gen-keyed ack shape. Its fixture row now
carries `session_id: 2717-aaaa`; it still asserts the pin reads row gen 11 and
`gen_after == 11`, and now asserts the ack lands at the session-id-keyed
`director-seat.ack.2717-aaa.json` (clause (1) IDENTITY shape) rather than at
`seats/<seat>.ack.json`.

## Evidence

Pre-fix measurement (old `_rename_own_window` + old seam, fixture
`@9 adv` + stale `@7 adv.prev`):

```
pre-fix window file       : ['@9', 'adv', '@7', 'adv.prev']
pre-fix own_window id     : @7      <- the STALE window, first-match-by-name
pre-fix stale survives    : True
```

Post-fix, the new negative test asserts:

```
own_id == @9                       (captured at the rename)
lines == ["@9 adv.prev"]           (exactly ONE .prev, the stale killed)
_successor_window_id("adv.prev") == @9
stale-only fixture -> no .prev survives (pred_alive can never report it live)
```

Commands and results (from the repo root of this worktree):

```
python3 -m pytest extensions/agi/tests/test_rotate_g1517.py -q
  -> 7 passed
python3 -m pytest extensions/agi/tests/test_rotate.py \
  extensions/agi/tests/test_rotate_handover.py \
  extensions/agi/tests/test_rotate_recover.py \
  extensions/agi/tests/test_rotate_startup.py \
  extensions/agi/tests/test_after_join_service.py -q
  -> 526 passed
python3 -m pytest extensions/agi/tests/test_rotate_selfreap.py \
  extensions/agi/tests/test_rotate_tail.py \
  extensions/agi/tests/test_rotate_autopsy.py -q
  -> 73 passed
python3 -m pytest extensions/agi/tests/test_heal_watch.py -q
  -> 63 passed
```

Files changed: `extensions/agi/bin/rotate.py` (spawn-pin/rename helper, the
handover capture site), `extensions/agi/tests/test_rotate_g1517.py` (the
migration + the new negative test). No record composition, no status/meter/whois
reader, no `posts.md` cell, no template touched.

## Agent Notes

- (0b) lands and is green. NOT covered by this kid: (0a) the spawn-pin handoff
  fallback (`_spawn_gen` still comes from `_seat_row_generation` alone,
  rotate.py:1921-1923), (0c) the `posts.md` `label_word` cells / unset lines,
  clause (2) RECORDS and clause (7) READERS, and the deprecation of the empty
  scaffold `experiment:a00-ab93dde5-a99e96`. Those belong to the sibling kids
  of this round; this kid deliberately stayed on one clause.
- `experiment:a00-ab93dde5-a99e96` is still LIVE under
  `.agi/nodes/experiment/` in this worktree (not deprecated here).
- A pre-existing pytest gate quirk: `pytest <file>::<test>` refuses with
  "AGI_TIER=kid refuses a bare full-suite directory run" while
  `pytest <file>` runs the same node fine — reported, not worked around.

## Agent Notes
clause (0b) built: _rename_own_window kills a stale <seat>.prev by @id before the rename and returns the own @id captured at the rename (threaded into handover.own_window.id); seam _replace_window_name preserves the @id; negative test added; g1517 ack test migrated to the session-id key. 7 + 526 + 73 + 63 passed.

PARENT REVIEW (a00-0866334b, SM.243): accepted for clause (0b) + the g1517 migration only. Bytes read: rotate.py _rename_own_window now kills a stale <seat>.prev resolved BY @id before the rename and returns the own @id captured pre-rename; _replace_window_name rewrites @<id> <old> -> @<id> <new>; cmd_rotate_self threads _renamed_own_id into handover own_window.id. Test migration is correct (session_id added to the fixture row, ack asserted at the session-keyed path, pin still 11, gen_after 11) and 526 tests across the five rotate suites plus g1517 are green. PARENT PROBE (gate, named): with a PLAIN-NAME stale line "adv\\nadv.prev" and no @id, _rename_own_window("adv","adv.prev") returns None and leaves TWO adv.prev lines (measured), so the blanket claim "afterwards new_name names exactly ONE window" holds only when an @id resolves. Production tmux always carries an @id, so this is a SEAM-ONLY gap and not a disprove, but the node claim is narrowed accordingly: uniqueness is @id-gated. NOT DELIVERED by this kid (left to later kids): clause (0a) spawn-pin, clause (0c) posts.md label_word cells + generation-unset lines, and the experiment:a00-ab93dde5-a99e96 deprecation.
