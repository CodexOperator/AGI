---
id: experiment:a00-18f83bf8-678f1d
mint_id: 00d2a51a3f3643dc933b4f0d87bd1975
type: experiment
parents:
  - hypothesis:l4-role-resolution-longest-prefix
next_edges: []
confidence: 0.8
edited_by: a00-5125c2a4
evidence_runs:
  - experiment:a00-18f83bf8-678f1d
loop: hypothesis:l4-role-resolution-longest-prefix@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 918c5f64b439308e
season: 2
title: A00 18f83bf8 678f1d
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-18f83bf8-678f1d

## Experiment

Implemented `hypothesis:l4-role-resolution-longest-prefix` in
`extensions/agi/bin/write.py`. The enforcer now compares a RESOLVED ROLE, never
the actor string.

New helpers in write.py:
- `_load_seats(root)` — reads the `seats:` rows of `.agi/nodes/.geometry/seats.md`
  (config:seats), a mirror of rotate.py's loader.
- `_pick_longest_role(candidates)` — longest-match wins; a tie at the same
  longest length raises `EditError` (fail-closed).
- `_resolve_seats_role(root, actor)` — a seat row matches only when the actor
  EQUALS the row name or starts with the row name FOLLOWED BY `-`. Longest match
  wins.
- `_resolve_role(root, actor, role_param)` — resolution order: (1) explicit
  `--role`; (2) `AGI_ROLE` env; (3) the seats prefix row; (4) literal actor
  `owner` -> role `owner`; (5) `""` UNRESOLVED.

`_enforce_written_by(root, node_type, actor, where, role)` now resolves the role
and refuses only when the type's schema declares `written_by` and the resolved
role is not admitted. An UNRESOLVED identity refuses because the type declares
`written_by`; a schema declaring nothing gates nothing (early return on falsy
`admitted`). The refusal message names the node TYPE and the admitted roles —
never a hardcoded type literal (L4.40 held).

Threaded `role` through `submit()` and `create()` (new `role=""` param) and
added a `--role` CLI flag to `main()`.

Two PRE-EXISTING tests encoded the old bug — a raw actor string (`scribe`,
`corrector`) admitted merely by matching an admitted writer with no resolution.
That is exactly the comparison L4.41 forbids, so they were updated to pass an
explicit `role=` (message-shape intent preserved).

## Evidence

Added 8 tests in `extensions/agi/tests/test_write.py`:
- (a) `belam-S1-L4-II` admits via seat->prime_director; `sanctuary-director-4e`
  refused (seats fixture, schema admitting [owner, prime_director]).
- (b1) `--role` beats AGI_ROLE; (b2) AGI_ROLE beats seats; (b3) seats beats the
  `owner` literal; (b4) literal actor `owner` -> role owner.
- (c) longest-prefix: rows `alive`/`alive-x`, actor `alive-x-1` resolves through
  `alive-x`, not `alive`.
- (d) boundary: `aliveness-bot` does NOT resolve through row `alive`.
- (e) tie at the longest length refuses (tested directly on
  `_pick_longest_role` — see caveat below).
- (f) a type declaring no `written_by` admits an unresolved actor as today.
- (g) `[moral]` still refuses a non-owner actor end to end (with a
  `sanctuary-director` seat row present, so no seat bypass).

Command: `python3 -m pytest extensions/agi/tests/test_write.py
extensions/agi/tests/test_links.py extensions/agi/tests/test_write_guard.py
extensions/agi/tests/test_node_writer.py extensions/agi/tests/test_unify.py -q`

Result: **257 passed, 0 failed** (194 in the four named files + 63 test_unify).
`write.py --help` shows `--role ROLE`; module syntax checks clean.

## Agent Notes
Implemented role resolution in write.py: _enforce_written_by now compares a resolved role (--role > AGI_ROLE > config:seats longest-prefix-with-boundary > owner literal > UNRESOLVED), tie refuses fail-closed, refusal names type+roles, no real schema touched. 8 new tests, 257 green. Two old tests encoding raw-actor admission updated to use --role.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (L4.41, a00-5125c2a4): accepted. Verified independently — 194 passed in the four named test files in this worktree; links.py reports 0 broken; git shows only write.py + test_write.py + this node touched, no real schema, no seats.md. The two updated pre-existing tests are legitimate: they admitted a raw actor string with no resolution, which is exactly what this round forbids, and their message-shape intent survives via explicit --role. The tie test (e) is unit-level on _pick_longest_role, not end-to-end — the kid honestly flagged that a tie is structurally unreachable through the boundary rule, so there is no end-to-end path to test it through. Accepted as proved: claim is (resolver compares a resolved role, fail-closed) and the implementation plus 8 fixture tests demonstrate it. The hypothesis listed 3 kids as ceiling; one sufficed, so no further spawn.
<!-- THOUGHT:END -->
